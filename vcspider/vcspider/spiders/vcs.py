# import scrapy as s
from vcspider.items import VcspiderItem
from vcspider.globals import domains, urls
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
# from scrapy.utils.response import get_base_url
import lxml.html as lh, lxml.etree as le
import lxml.html as lh
import lxml.etree as le
import re
from goose import Goose

# import logging
# from scrapy.log import ScrapyFileLogObserver
# from twisted.python import log
# import logging
# logging.basicConfig(level=logging.ERROR, filemode='w', filename='vcerror_log.txt')


class VcSpider(CrawlSpider):
    name = "vcs"
    allowed_domains = domains
    start_urls = urls

    rules = (
        Rule(LinkExtractor(), callback='parse_items', follow=True),
    )

    g = Goose()

    def parse_items(self, response):

        fulltext = self.parse_body_text(response)
        gooseobj = self.g.extract(response.url)
        fulltext = gooseobj.cleaned_text
        # fulltext = self.parse_body_text(response)

        il = ItemLoader(item=VcspiderItem(), response=response)
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

# meta[@name="keywords"]/@content
    # base access method
    # def parse_items(self, response):
        # hxs = s.Selector(response)
        # item = VcspiderItem()
        # text = ''.join(hxs.xpath("//body//text()").extract()).strip()
        # item['page'] = hxs.xpath("//title//text()").extract()
        # item['text'] = text
        # items.append(item)
        # return(item)


# for titles in titles:
#             item = VcspiderItem()
#             item['title'] = titles.xpath('a/text()').extract()
#             item['link'] = titles.xpath('a/@href').extract()
#             items.append(item)
#
#         return(items)


#     def parse_page(self, response):
#         item = VcspiderItem()
#         sel = response.xpath('//html')
#         text = ''.join(sel.xpath("//body//text()").extract()).strip()
#         item['site'] = 'tgc'
#         item['text'] = text
#         yield item




#     def parse(self, response):
#         sel = Selector(response)
#         sites = sel.xpath('//div[@id="menu"]')
#         items = []
#
#         for site in sites:
#             item = VcspiderItem()
#             item['name'] = site.xpath('a/text()').extract()
#             item['url'] = site.xpath('a/@href').extract()
#             items.append(item)
#
#         with open('./links.txt', 'w') as l:
# 			for item in items:
# 				l.write(items)
#
#         yield items
