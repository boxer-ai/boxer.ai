import scrapy


class VcspiderItem(scrapy.Item):
    text = scrapy.Field(default = 'none')
    siteurl = scrapy.Field()
    pageurl = scrapy.Field()
    # keywords = scrapy.Field()
    pagetitle = scrapy.Field(default = 'none')

    pass
