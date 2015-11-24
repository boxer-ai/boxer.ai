from flask import Flask, g, session
from flask import render_template, flash, redirect, url_for
from flask import request
from .forms import SiteForm
from flask.ext.session import Session
from celery import Celery, task

import re
import ast
import mysql.connector as msc
from collections import namedtuple
import cortipy
from scrapy.crawler import CrawlerProcess
from vcspider.vcspider.spiders import solo
from vcspider.vcspider.pipelines import UserInputPipeline
# from flask.ext.mysqldb import MySQL
from flask.ext.mysql import MySQL
import time
from flask.ext.sqlalchemy import SQLAlchemy

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

# db = SQLAlchemy(app)
# db.create_all()
mysql = MySQL()
mysql.init_app(app)

client = cortipy.CorticalClient(app.config['CORTIPY_API_KEY'])

Site = namedtuple('Site', 'siteurl text')
CSite = namedtuple('CorticalSite', 'siteurl text fingerprint keywords')

@celery.task()
def scrape(siteurl): 
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'app.vcspider.vcspider.pipelines.UserInputPipeline': 100},
        'DEPTH_LIMIT': 2,
        'DOWNLOAD_HANDLERS': {'s3': None,}
    })
    process.crawl(solo.SoloSpider, domain = siteurl)
    process.start()

def get_site(siteurl):
    """
    Either scrapes text of input site, or returns already-scraped data.
    """
    con = mysql.connect()
    cur = con.cursor()

    sql = 'SELECT text FROM crunchbase_startups WHERE siteurl = %s'
    cur.execute(sql, (siteurl,))
    text = cur.fetchone()
    con.commit()

    if text != None:
        flash('Site already scraped, proceeding with analysis...')

        sql = 'SELECT siteurl, text, cortical_io, cortical_io_keywords FROM crunchbase_startups WHERE siteurl = %s'

        cur.execute(sql, (siteurl,))
        _, _, fingerprint, keywords = cur.fetchone()

        con.commit()
        fingerprint = ast.literal_eval(fingerprint) 
        if isinstance(fingerprint, dict): fingerprint = fingerprint['positions'] # this is dumb, fix later

        return CSite(siteurl, text, fingerprint, [keywords])

    else: # scrape site
        flash('Trying to scrape site: {}'.format(siteurl))
        scraper = scrape.delay(siteurl)

        # loop until results are populated
        while text == None:
            cur.execute(sql, (siteurl,))
            text = cur.fetchone()
            con.commit()
            time.sleep(1) # wait to try again

        return Site(siteurl, text)

def getSDRDist(site1, site2, metric = 'euclideanDistance'):
    # flash('1: {}, type = {}'.format(site1.fingerprint, type(site1.fingerprint)))
    # flash('2: {}, type = {}'.format(site2.fingerprint, type(site2.fingerprint)))
    return client.compare(site1.fingerprint, site2.fingerprint)[metric]

def makeSDR(siteurl, text):
    site_corticalmap = client.createClassification(siteurl, [text[0]], "")
    site_keywords = client.extractKeywords(text[0])

    # write to db
    con = mysql.connect()
    cur = con.cursor()

    sql = """UPDATE crunchbase_startups
            SET cortical_io = %s, cortical_io_keywords = %s
            WHERE  siteurl = %s"""

    cur.execute(sql, (str(site_corticalmap), ','.join(site_keywords), siteurl))
    con.commit()
    # flash(cur._executed)

    return CSite(siteurl, text, site_corticalmap['positions'], [site_keywords])

def getMatch(startup):
    # this needs to grab all from db once and then get dist one-by-unfortunate-one
    # fix later
    con = mysql.connect()
    cur = con.cursor()

    sql = """SELECT siteurl, text, cortical_io, cortical_io_keywords 
    FROM vctest4
    WHERE 
        NULLIF(text, '') IS NOT NULL 
        AND NULLIF(cortical_io, '') IS NOT NULL
    ORDER BY RAND() LIMIT 1"""

    cur.execute(sql)
    con.commit()
    siteurl, text, fingerprint, keywords = cur.fetchone()
    fingerprint = map(int, re.sub(r'[\]\'\[]', '', fingerprint).split(',')) # convert from db str repr to list
    vc = CSite(siteurl, text, fingerprint, keywords)
    # getSDRDist(startup, vc)
    # return 0
    return {'vc': vc.siteurl, 'dist': getSDRDist(startup, vc)}


###############
# BEGIN VIEWS #
###############

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            title = 'Home',
                            h1 = "active",
                            h2 = "inactive",
                            h3 = "inactive")

@app.route('/about')
def about():
    return render_template('about.html',
                            title = 'About',
                            h1 = "inactive",
                            h2 = "active",
                            h3 = "inactive")

@app.route('/contact')
def contact():
    return render_template('contact.html',
                            title = 'Contact',
                            h1 = "inactive",
                            h2 = "inactive",
                            h3 = "active")  

@app.route('/process', methods=['GET', 'POST'])
def process():

    siteurl = request.args.get('url')
    sitedata = get_site(siteurl)

    if isinstance(sitedata, Site):
        sitedata = makeSDR(sitedata.siteurl, sitedata.text)

    flash('Keywords for site {}: {}'.format(sitedata.siteurl, sitedata.keywords))
    flash('Getting best match...')

    best = {'vc': 'na', 'dist': 0}

    for x in xrange(1500): # THIS IS DUMB YES
        # flash('In loop.')
        dt = getMatch(sitedata)
        # flash('VC: {}, distance: {} (best dist = {}'.format(dt['vc'], dt['dist'], best['dist']))

        if dt['dist'] > best['dist']:
            best = dt

    flash('Best VC: {}, with dist = {}'.format(best['vc'], best['dist']))

    return render_template('process.html',
                            title = 'Results',
                            h1 = "inactive",
                            h2 = "inactive",
                            h3 = "inactive")  

@app.route('/input', methods=['GET', 'POST'])
def input():
    form = SiteForm(request.form)

    if request.method == 'POST' and form.validate():        
        return redirect(url_for('process'))

    return render_template('input.html', 
                            title = 'Enter site',
                            h1 = "inactive",
                            h2 = "inactive",
                            h3 = "inactive",
                            form = form)   






