import re
import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from goose import Goose

def parse_base_url(url):
   url = re.sub(r'((http(s)?://)?(www.)?)', '', url.lower())  # strip head
   print url.find('/')
   return url[:url.find('/')] if url.find('/') != -1 else url

class SoloSpider(CrawlSpider):
    name = "solo"

    rules = (Rule(LinkExtractor(), callback='parse_items', follow=True),)

    def __init__(self, **kw):
        super(SoloSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('domain')

        self.g = Goose()
        self.url = url
        self.allowed_domains = [url]
        self.start_urls = ['http://www.' + url]

    def parse_items(self, response):

        gooseobj = self.g.extract(response.url)
        fulltext = gooseobj.cleaned_text

        il = ItemLoader(item=SoloItem(), response=response)
        il.default_output_processor = MapCompose(
            lambda v: v.rstrip(),
            lambda v: re.sub(r'[\',|!]', '', v),
            lambda v: re.sub(r'\s+', ' ', v)
        )

        il.add_value('siteurl', parse_base_url(response.url))
        il.add_value('pageurl', response.url)
        il.add_value('text', fulltext.encode('ascii', 'ignore'))
        il.add_xpath('pagetitle', '//title/text()')

        return il.load_item()

def ScrapeSite():
    db = 'crunchbase_startups'
    sitedomain = raw_input("Enter site domain: ") # get user input
    sitedomain = parse_base_url(sitedomain) # clean url
    
    sql = 'SELECT text FROM {} WHERE siteurl = %s'.format(db)
    
    cur.execute(sql, sitedomain)
    sitetext = cur.fetch()
    
    if sitetext != '': # what does an empty ping return?
        print 'Site already scraped.'
        return sitetext
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'pipelines.UserInputPipeline': 100},
        'DEPTH_LIMIT': 2,
        'DOWNLOAD_HANDLERS': {'s3': None,}
        ,'LOG_LEVEL': 'INFO'
    })
    
    process.crawl(SoloSpider, domain = sitedomain)
    process.start()
    
    # presumably finished here - pull newly loaded sitetext for domain
    
    cur.execute(sql, sitedomain)
    return cur.fetch()


def InputText():
    textdesc = raw_input("Please enter a description of your startup / product:")
    return textdesc



if __name__ == "__main__":

    config = MYSQL_GSA_CONFIG # yes yes it's dumb, this will change later anyway
    con = msc.connect(**config)
    cur = con.cursor()

    # flask forthcoming

    print """Welcome to M^3!\n\nThis tool generates a \"digital fingerprint\" of your startup based on the available
    text of your website. Optionally, you may enter a description of your product yourself.\n
    Please select from one of the following options:
    \t 1) Input your website
    \t 2) Enter a text description of your startup\n"""

    comparetype = raw_input()

    inputtext = ScrapeSite() if comparetype == '1' else InputText()

    print inputtext


