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
import numpy as np
from collections import namedtuple
from operator import itemgetter

import mysql.connector as msc
import cortipy
from scrapy.crawler import CrawlerProcess
from vcspider.vcspider.spiders import solo
from vcspider.vcspider.pipelines import UserInputPipeline


"""
This code needs a lot of cleaning. It's okay periodically, but is generally haphazard,
mirroring its genesis.
"""

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
app.config.from_object('config') # mysql conn, cortical api key

# celery uses redis as a broker, must have redis server running on machine!
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app) # init celery

# flask-specific mysql interface
mysql = MySQL()
mysql.init_app(app)

# seeeeecret key. get your own.
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

def makeSDR(text, siteurl = 'TextInput', isText = 0):
    """
    Makes an SDR and associated keywords for input site or text.
    """

    site_corticalmap = client.createClassification(siteurl, [text[0]], "")
    site_keywords = client.extractKeywords(text[0])

    # write to db
    con = mysql.connect()
    cur = con.cursor()

    if isText == 0:
        sql = """UPDATE crunchbase_startups
                SET cortical_io = %s, cortical_io_keywords = %s
                WHERE  siteurl = %s"""

        cur.execute(sql, (str(site_corticalmap), ','.join(site_keywords), siteurl))

    elif isText == 1:
        sql = """INSERT INTO sitedescriptions (text, cortical_io, cortical_io_keywords)
                VALUES (%s, %s, %s)"""

        cur.execute(sql, (text, str(site_corticalmap), ','.join(site_keywords)))

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

def eucDist(l1, l2):
    """The Euclidean distance is defined as a float between 0 and 1, 0 representing a 
    smaller distance and thus closer match between two SDRs. It is calculated as 
    the quotient of the length of the symmetric difference between two sets and the
    total length of the combined sets."""

    totlen = len(l1) + len(l2)
    sublen = len(set(l1) ^ set(l2))

    return sublen / totlen


def cosSim(l1, l2):
    """Here (and only here, per cortical.io), cosine similarity is defined as a float 
    between 0 and 1, 1 representing a high similarity. It is calculated as the 
    quotient of the length of the number of bits contained in both sets and the square 
    root of len(l1) * len(l2)."""

    overlap = len(set(l1) & set(l2))
    totsize = len(l1) * len(l2)

    return overlap / np.sqrt(totsize)

def getMatch(startup):
    """Find top three matches for the given startup based on both Euclidean distance
    and Cosine similarity (calculated per cortical's API, not really mappable to 
    traditional definitions, ESPECIALLY cosine similarity.)
    """

    vcList = loadVCList()
    scoresEuc, scoresCos = list(), list()

    for vc in vcList:
        # euclidean
        scoreEuc = eucDist(startup.fingerprint, ast.literal_eval(vc[1]))
        scoresEuc.append(tuple([vc[0], scoreEuc]))

        # cosine
        scoreCos = cosSim(startup.fingerprint, ast.literal_eval(vc[1]))
        scoresCos.append(tuple([vc[0], scoreCos]))

    scoresEuc = sorted(scoresEuc, key = itemgetter(1))
    scoresCos = sorted(scoresCos, key = itemgetter(1), reverse = True)
    
    flash('Euclidean: {}'.format(scoresEuc[:3]))
    flash('Cosine: {}'.format(scoresCos[:3])) 

    return tuple((scoresEuc, scoresCos))

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

    descr = request.args.get('descr')

    if descr == 'y':
        siteinput = request.args.get('siteinput')
        sitedata = makeSDR(tuple((siteinput,)), isText = 1) # this tuple is awful

    elif descr == None:
        siteurl = request.args.get('siteinput')
        sitedata = get_site(siteurl)

        if isinstance(sitedata, Site):
            sitedata = makeSDR(sitedata.text, sitedata.siteurl)


    flash('Keywords for site {}: {}'.format(sitedata.siteurl, sitedata.keywords))
    flash('Getting best match...')

    matches = getMatch(sitedata)

    return render_template('process.html',
                            title = 'Results',
                            h1 = "inactive", h2 = "inactive", h3 = "inactive",
                            )  

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






