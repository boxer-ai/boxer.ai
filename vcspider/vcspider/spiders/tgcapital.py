import scrapy as s
from vcspider.items import VcspiderItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor

items = []

class TGCapSpider(CrawlSpider):
    name = "tgcap"
    allowed_domains = ["3g-capital.com"]
    start_urls = [
        "http://www.3g-capital.com/"
    ]
    
    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_items', follow= True),
    )

    def parse_items(self, response):
        hxs = s.Selector(response)
        item = VcspiderItem()
         
        text = ''.join(hxs.xpath("//body//text()").extract()).strip()
        item['page'] = hxs.xpath("//title//text()").extract()
        item['text'] = text
        items.append(item)
        return(item)
        
        

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
		
	
