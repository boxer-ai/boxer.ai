from vcspider.items import SuspiderItem
from vcspider.globals import domains_su, urls_su
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import lxml.html as lh
import lxml.etree as le
import re

from goose import Goose


class SuSpider(CrawlSpider):
    name = "sus"
    allowed_domains = domains_su
    start_urls = urls_su

    rules = (
        Rule(LinkExtractor(), callback='parse_items', follow=True),
    )

    g = Goose()

    def parse_items(self, response):

        # fulltext = self.parse_body_text(response)
        gooseobj = self.g.extract(response.url)
        fulltext = gooseobj.cleaned_text

        il = ItemLoader(item=SuspiderItem(), response=response)
        il.default_output_processor = MapCompose(
            lambda v: v.rstrip(),
            lambda v: re.sub(r'[\',|!]', '', v),
            lambda v: re.sub(r'\s+', ' ', v)
        )

        il.add_value('siteurl', self.parse_base_url(response.url))
        il.add_value('pageurl', response.url)
        il.add_value('text', fulltext.encode('ascii', 'ignore'))
        il.add_xpath('pagetitle', '//title/text()')
        # il.add_xpath('keywords', '//meta[@name="keywords"]/@content')

        yield il.load_item()

    def parse_body_text(self, response):

        root = lh.fromstring(response.body)
        le.strip_elements(root, le.Comment, 'script', 'head', 'a')
        fulltext = lh.tostring(root, method="text", encoding=unicode)
        fulltext = fulltext.strip().replace('\n', '')
        fulltext = re.sub(r'\s+', ' ', fulltext)

        yield fulltext

    def parse_base_url(self, url):
        url = re.sub(r'((http(s)?://)?(www.)?)', '', url.lower())  # strip head
        yield url[:url.find('/')]

# ItemLoader vs normal Item access methods - can you get whole corpus?


