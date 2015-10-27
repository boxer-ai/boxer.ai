import scrapy


class VcspiderItem(scrapy.Item):
#     define the fields for your item here like:
    page = scrapy.Field()
    text = scrapy.Field()
    
    pass
