import scrapy


class VcspiderItem(scrapy.Item):
    text = scrapy.Field()
    siteurl = scrapy.Field()
    pageurl = scrapy.Field()
    # keywords = scrapy.Field()
    pagetitle = scrapy.Field()

    pass
