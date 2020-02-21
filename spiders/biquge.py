# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider
from Biqugebook.utils.common import get_md5
from Biqugebook.items import BiqugebookItem
import datetime


class BiqugeSpider(RedisSpider):
    name = 'biquge'
    #allowed_domains = ['www.xbiquge.la']
    redis_key = "biquge:start_urls"

    def parse(self, response):
        for li in response.xpath('//*[@id="newscontent"]/div[1]/ul/li'):
            know = dict()
            book_url = li.css('.s2 a::attr(href)').extract_first('')
            know['style'] = li.css('.s1::text').extract_first('').replace('[', '').replace(']', '')
            know['name'] = li.css('.s2 a::text').extract_first('')
            know['author'] = li.css('.s4::text').extract_first('')
            yield scrapy.Request(url=urljoin(response.url, book_url), callback=self.parse_detail, meta=know)

    def parse_detail(self, response):
        item = BiqugebookItem()
        item['name'] = response.meta.get('name')
        item['author'] = response.meta.get('author')
        item['style'] = response.meta.get('style')
        item['url_md5'] = get_md5(response.url)
        item['book_image'] = [response.xpath('//*[@id = "fmimg"]/img/@src').extract_first('')]
        item['book_intro'] = response.xpath('//*[@id = "intro"]/p[2]/text()').extract_first('').strip()
        try:
            update_time = response.xpath('//*[@id = "info"]/p[3]/text()').extract_first('').replace('最后更新：', '').strip()
            item['update_time'] = datetime.datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S')
        except:
            item['update_time'] = datetime.datetime.now()
        item['last_page'] = response.xpath('//*[@id = "info"]/p[4]/a/text()').extract_first('')
        item['biqugecol'] = datetime.datetime.now()
        yield item
