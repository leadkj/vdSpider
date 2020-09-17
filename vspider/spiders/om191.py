import scrapy
from vspider.items import VspiderItem
from scrapy.http.request import Request
import js2xml
from js2xml.utils.vars import get_vars
import re
from fake_useragent import UserAgent
ua = UserAgent()


class Om191Spider(scrapy.Spider):
    name = 'xyz'
    allowed_domains = ['xyz.com']
    start_urls = ['http://www.xyz.com/index.php/vod/type/id/4.html']
    domain = 'http://www.xyz.com'
    custom_settings = {
        "ITEM_PIPELINES": {
            'vspider.pipelines.VspiderPipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "http://www.fq191.com",
            'User-Agent':ua.random
        }
    }


    def parse(self,response):
        vds = response.xpath('//div[@class="xl12"]/div/div')
        for vd in vds:
            item = VspiderItem()
            item['name'] = vd.xpath('div/div/a/@title').get()
            item['image_url']  =  vd.xpath('div/div/a/img/@src').get()
            url = self.domain +vd.xpath('div/div/a/@href').get()
            item['page_url'] = url

            yield  Request(url=url,callback=self.get_vd_url,meta={'item':item})
        next = response.xpath('//div/a[contains(text(), "下一页")]/@href').get()
        if next:
            next_url = self.domain+next
            print("    "+next_url+"\n")
            yield Request(url=next_url,callback=self.parse)

    def get_vd_url(self,responese):
        iframe_url = responese.xpath('//script[1]/text()').get()
        item = responese.meta['item']
        res = get_vars(js2xml.parse(iframe_url))
        item['iframe_url'] = res['player_data']['url']

        yield Request(url=item['iframe_url'],callback=self.get_m3u8_url,meta={'item':responese.meta['item']},dont_filter = True)

    def get_m3u8_url(self,responese):
        m3u8_url = responese.xpath('normalize-space(//script[8])').get()
        res = re.findall(r'\[{"url":"(.+)"}\]',m3u8_url)
        item = responese.meta['item']
        item['m3u8_url'] =re.findall(r'(htt.+com)/',item['iframe_url'])[0]+ res[0]
        yield  item

