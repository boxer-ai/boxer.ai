import re
from ..items import SoloItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from goose import Goose

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
        # self.link_extractor = LinkExtractor()

    def parse_items(self, response):

        # print 'PARSE ITEMS'
        gooseobj = self.g.extract(response.url)
        fulltext = gooseobj.cleaned_text

        il = ItemLoader(item=SoloItem(), response=response)
        il.default_output_processor = MapCompose(
            lambda v: v.rstrip(),
            lambda v: re.sub(r'[\',|!]', '', v),
            lambda v: re.sub(r'\s+', ' ', v)
        )

        il.add_value('siteurl', self.parse_base_url(response.url))
        il.add_value('pageurl', response.url)
        il.add_value('text', fulltext.encode('ascii', 'ignore'))
        il.add_xpath('pagetitle', '//title/text()')

        yield il.load_item()

    def parse_base_url(self, url):
       url = re.sub(r'((http(s)?://)?(www.)?)', '', url.lower())  # strip head
       # print url.find('/')
       return url[:url.find('/')] if url.find('/') != -1 else url