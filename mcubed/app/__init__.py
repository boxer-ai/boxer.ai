from __future__ import division

from flask import Flask, g, session
from flask import render_template, flash, redirect, url_for
from flask import request
from .forms import SiteForm
from flask.ext.session import Session
from celery import Celery, task
from flask.ext.mysql import MySQL
from flask.ext.sqlalchemy import SQLAlchemy

import re
import ast
import time
from collections import namedtuple
from operator import itemgetter

import mysql.connector as msc
import cortipy
from scrapy.crawler import CrawlerProcess
from vcspider.vcspider.spiders import solo
from vcspider.vcspider.pipelines import UserInputPipeline


def make_celery(app):
    """
    Init celery environment with Redis broker. Allows use of celery decorator.
    """

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

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

mysql = MySQL()
mysql.init_app(app)

client = cortipy.CorticalClient(app.config['CORTIPY_API_KEY'])

# some light-weight data structures
Site = namedtuple('Site', 'siteurl text')
CSite = namedtuple('CorticalSite', 'siteurl text fingerprint keywords')

@celery.task()
def scrape(siteurl): 
    """
    Initializes Scrapy crawler for given siteurl. See spider/pipeline code for more.
    """

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

    sql = """SELECT text FROM crunchbase_startups WHERE siteurl = %s"""
    cur.execute(sql, (siteurl,))
    text = cur.fetchone()
    con.commit()

    if text != None: # if site already scraped
        flash('Site already scraped, proceeding with analysis...')

        sql = """SELECT siteurl, text, cortical_io, cortical_io_keywords 
                FROM crunchbase_startups WHERE siteurl = %s"""

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
    """
    Now just for QA, get API distance
    """

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

    return CSite(siteurl, text, site_corticalmap['positions'], [site_keywords])

def loadVCList():
    """Get all VCs for comparison to selected startup."""

    # i shouldn't be re-initializing this everywhere...
    con = mysql.connect()
    cur = con.cursor()

    # load ALL VCs into memory - not site text, so it's manageable
    sql = """SELECT siteurl, cortical_io, cortical_io_keywords 
    FROM vctest4
    WHERE 
        NULLIF(text, '') IS NOT NULL 
        AND NULLIF(cortical_io, '') IS NOT NULL
    ORDER BY RAND()"""

    cur.execute(sql)
    con.commit()

    vcList = cur.fetchall() 

    return vcList 

def getMatch(startup):
    """Find top three matches for the given startup based on the Euclidean distance
    of two SDRs.

    The Euclidean distance is defined as a float between 0 and 1, 0 representing a 
    smaller distance and thus closer match between two SDRs. It is calculated as 
    the quotient of the length of the symmetric difference between two sets and the
    total length of the combined sets. Ie:

    score = len(s ^ t) / (len(s) + len(t))
    """

    vcList = loadVCList()
    scores = list()

    # add more distance metrics and eval?
    for vc in vcList:
        totlen = len(startup.fingerprint) + len(ast.literal_eval(vc[1]))
        sublen = len(set(startup.fingerprint) ^ set(ast.literal_eval(vc[1])))
        score = sublen / totlen

        scores.append(tuple([vc[0], score]))

    scores = sorted(scores, key = itemgetter(1))
    flash(scores[:3]) # returning top three scores
    return scores

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

    # flash('Keywords for site {}: {}'.format(sitedata.siteurl, sitedata.keywords))
    flash('Getting best match...')

    matches = getMatch(sitedata)

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






