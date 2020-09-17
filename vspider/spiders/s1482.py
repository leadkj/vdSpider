import scrapy
from vspider.items import VspiderItem, S1482Item
from scrapy.http.request import Request
import js2xml
from js2xml.utils.vars import get_vars
import re
from fake_useragent import UserAgent
ua = UserAgent()


class S1482Spider(scrapy.Spider):
    name = 'abcdefg'
    allowed_domains = ['abcdefg.com']
    start_urls = ['http://www.abcdefg.com/?m=vod-type-id-3-pg-98.html']
    domain = 'http://www.abcdefg.com'
    custom_settings = {
        "ITEM_PIPELINES": {
            'vspider.pipelines.S1482Pipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "http://www.abcdefg.com",
            'User-Agent':ua.random
        }
    }


    def parse(self,response):
        vds = response.xpath('//ul[@id="content"]/li')
        for vd in vds:
            item = S1482Item()
            item['name'] = vd.xpath('a/@title').get()
            item['image_url']  =  vd.xpath('a/@data-original').get()
            url = self.domain +vd.xpath('a/@href').get()
            item['page_url'] = re.sub(r'.html','-src-1-num-1.html',re.sub('detail','play',url))

            yield  Request(url=item['page_url'],callback=self.get_vd_url,meta={'item':item})
        next = response.xpath('//ul/a[contains(text(), "下一页")]/@href').get()
        if next:
            next_url = self.domain+next
            print("    "+next_url+"\n")
            yield Request(url=next_url,callback=self.parse)

    def get_vd_url(self,responese):
        item = responese.meta['item']
        iframe_url = responese.xpath('//script[1]/text()').get()
        res = re.findall(r'unescape\(\'(.+)\'\);',iframe_url)[0]
        s1=res.replace('%u', r'\u')
        s2=s1.encode('utf-8').decode('unicode_escape')
        import urllib.parse
        s3=urllib.parse.unquote(s2)
        try:
            url = re.findall(r'\$(.*)\${3}',s3)[0]
        except Exception as e:
            url=None
        item['m3u8_url'] = re.findall(r'\${3}.*\$(.+)',s3)[0]
        item['iframe_url'] = url
        if url:
            yield Request(url=item['iframe_url'],callback=self.get_m3u8_url,meta={'item':responese.meta['item']},dont_filter = True)
        else:
            yield item
    def get_m3u8_url(self,responese):
        try:
            m3u8_url = responese.xpath('normalize-space(//script[8])').get()
            # print(m3u8_url)
            #
            res = re.findall(r'\[{"url":"(.+)"}\]',m3u8_url)
            item = responese.meta['item']
            item['m3u8_url'] =re.findall(r'(htt.+com)/',item['iframe_url'])[0]+ res[0]
        except Exception as e:
            pass
        yield  item

