import re
import mysql.connector as msc
from collections import namedtuple
import cortipy
from scrapy.crawler import CrawlerProcess
from vcspider.vcspider.settings import MYSQL_GSA_CONFIG, CORTIPY_API_KEY
from vcspider.vcspider.spiders import solo

def parse_base_url(url):
   url = re.sub(r'((http(s)?://)?(www.)?)', '', url.lower())  # strip head
   print url.find('/')
   return url[:url.find('/')] if url.find('/') != -1 else url

def ScrapeSite():
    """
    Get user site, check if that domain has already been scraped. If not, scrape it.
    Returns a tuple of siteurl and text.
    """

    db = 'crunchbase_startups'
    sitedomain = raw_input("Enter site domain: ") # get user input
    sitedomain = parse_base_url(sitedomain) # clean url
    
    sql = 'SELECT text FROM {} WHERE siteurl = %s'
    sql = sql.format(db)

    cur.execute(sql, (sitedomain,))
    text = cur.fetchone()

    if text != None:
        print 'Site already scraped, proceeding with analysis...'

        sql = 'SELECT siteurl, text, cortical_io, cortical_io_keywords FROM {} WHERE siteurl = %s'
        sql = sql.format(db)

        cur.execute(sql, (sitedomain,))
        _, _, fingerprint, keywords = cur.fetchone()

        return CSite(sitedomain, text, fingerprint, keywords)
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'vcspider.vcspider.pipelines.UserInputPipeline': 100},
        'DEPTH_LIMIT': 2,
        'DOWNLOAD_HANDLERS': {'s3': None,}
        ,'LOG_LEVEL': 'INFO'
    })

    print 'Scraping your site...'
    process.crawl(solo.SoloSpider, domain = sitedomain)
    process.start()
    
    # pull newly scraped sitetext for domain
    cur.execute(sql, (sitedomain,))
    text = cur.fetchone()

    return Site(sitedomain, text)


def InputText():
    item = raw_input("Please enter the name of your startup / product: ")
    desc = raw_input("Please enter a description of your startup / product:")
    return Site(item, desc)

def getSDR(siteurl, text):
    site_corticalmap = client.createClassification(siteurl, [text], "")
    site_keywords = client.extractKeywords(text)

    return CSite(siteurl, text, site_corticalmap['positions'], [site_keywords])

# def saveSDR(siteurl, text):


def getSDRDist(site1, site2, metric = 'euclideanDistance'):
    return client.compare(site1.fingerprint, site2.fingerprint)[metric]

if __name__ == "__main__":
    Site = namedtuple('Site', 'siteurl text')
    CSite = namedtuple('CorticalSite', 'siteurl text fingerprint keywords')
    client = cortipy.CorticalClient(CORTIPY_API_KEY)

    config = MYSQL_GSA_CONFIG # yes yes it's dumb, this will change later anyway
    con = msc.connect(**config)
    con.autocommit = True

    cur = con.cursor()

    # flask forthcoming

    print """Welcome to M^3!\n\nThis tool generates a \"digital fingerprint\" of your startup based on the available
    text of your website. Optionally, you may enter a description of your product yourself.\n
    Please select from one of the following options:
    \t 1) Input your website
    \t 2) Enter a text description of your startup\n"""

    comparetype = raw_input()

    # returns full object or just sitename/text
    site = ScrapeSite() if comparetype == '1' else InputText()
    startup = \
        getSDR(site.siteurl, site.text[0]) if isinstance(site, Site) \
        else site

    print type(startup.fingerprint)
    print


