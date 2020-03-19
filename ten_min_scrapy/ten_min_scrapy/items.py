import scrapy

class Post(scrapy.Item):
    url   = scrapy.Field()
    title = scrapy.Field()
    date  = scrapy.Field()
