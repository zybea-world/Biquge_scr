# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BiqugebookItem(Item):
    # define the fields for your item here like:
    name = Field()
    author = Field()
    style = Field()
    url_md5 = Field()
    book_image = Field()
    book_image_path = Field()
    book_intro = Field()
    update_time = Field()
    last_page = Field()
    biqugecol = Field()

    def get_insert(self):
        lis = tuple(dict(self).values())
        index = ','.join(['% s']*len(lis))
        update = ','.join([key + '=%s' for key in dict(self)])
        sql = 'insert into biquge values ({index}) on duplicate key update {update}'.format(index=index,update=update)
        return lis,sql



