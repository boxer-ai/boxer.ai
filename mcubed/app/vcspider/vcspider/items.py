import scrapy


class VcspiderItem(scrapy.Item):
    text = scrapy.Field(default = 'none')
    siteurl = scrapy.Field()
    pageurl = scrapy.Field()
    # keywords = scrapy.Field()
    pagetitle = scrapy.Field(default = 'none')

class SuspiderItem(scrapy.Item):
    text = scrapy.Field(default = 'none')
    siteurl = scrapy.Field()
    pageurl = scrapy.Field()
    # keywords = scrapy.Field()
    pagetitle = scrapy.Field(default = 'none')

class SoloItem(scrapy.Item):
    text = scrapy.Field(default = 'none')
    siteurl = scrapy.Field()
    pageurl = scrapy.Field()
    pagetitle = scrapy.Field(default = 'none')