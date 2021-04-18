import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ehsy.items import EhsyItem


class EhsyspiderSpider(RedisSpider):
    name = 'ehsyspider'
    allowed_domains = ['ehsy.com']
    # start_urls = ['http://www.ehsy.com/']
    redis_key = "ehsyspider:start_urls"


    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(EhsyspiderSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        '''
        获取以及分类连接category_lv1_urls
        :param response:
        :return:
        '''
        for category_lv1 in response.xpath('//div[@class="menu-content-box js-menu-clone"]/ul/li/a'):
            item = EhsyItem()
            item['cat_name1'] = category_lv1.xpath('span/text()').get()
            cat_name1_url = category_lv1.attrib['href']
            item['cat_name1_url'] = cat_name1_url
            item['cat_name1_id'] = cat_name1_url.split("/")[-1]
            yield Request(url=cat_name1_url,callback=self.category_lv2_3_urls,meta={"item":item})



    def category_lv2_3_urls(self,response):
        '''
        获取二三级分类连接地址
        :param response:
        :return:
        '''

        for category_lv2 in response.xpath('//div[@class="cat-title-name"]'):
            item = response.meta['item']
            item['cat_name2'] = category_lv2.xpath('a/text()').get()
            cat_name2_url = category_lv2.xpath('a/@href').get()
            item['cat_name2_url'] = cat_name2_url
            item['cat_name2_id'] = cat_name2_url.split("/")[-1]
            for category_lv3 in response.xpath('//div[@class="nodeImg"]'):
                item['cat_name3'] = category_lv3.xpath('a/img/@title').get()
                cat_name3_url = category_lv3.xpath('a/@href').get()
                item['cat_name3_url'] = cat_name3_url
                item['cat_name3_id'] = cat_name3_url.split("-")[-1]
                yield Request(url=cat_name3_url,callback=self.product_urls,meta={"item":item})

    def product_urls(self,response):
        '''
        获取产品连接，部分属性信息和下一页连接
        :param response:
        :return:
        '''
        for product in response.xpath('//div[@class="product-list listMode"]/div'):
            item = response.meta['item']
            item['product_id'] = product.attrib['data-text']  #获取商品ID
            item['title'] = product.xpath('a/@title').get()  #获取商品名称
            product_url = product.xpath('a/@href').get()  #商品连接地址
            item['product_url'] = product_url
            item['brand']=''.join([i.get().strip() for i in product.xpath('ul/li[1]/text()')]) #获取品牌
            item['model'] = product.xpath('ul/li[2]/text()').get() #获取商品型号
            # item['price'] = product.xpath('ul/li[8]/span/span/text()').get()  #获取商品价格
            # item['stock'] = product.xpath('ul/li[9]/span/text()').get() #是否有库存
            yield Request(url=product_url,callback=self.parse_item,meta={"item":item})
        next_url = response.xpath('//div[@class="pagintion"]/ul/li[@class="pg-next"]/a/@href').get()
        if next_url:
            yield Request(url=next_url, callback=self.product_urls,meta=response.meta)

    def parse_item(self, response):
        '''
        解析产品详情页面数据，保存到item
        :param response:
        :return:
        '''
        item = response.meta['item']
        # item['title'] = response.xpath('//div[@calss="product-info-detail"]/h1/@title').get()
        # item['price']= 100
        # item['brand'] ="abcd"
        yield item
