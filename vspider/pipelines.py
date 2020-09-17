# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class VspiderPipeline:
    def __init__(self):
        self.db = pymysql.connect('192.168.10.100','root','pp123','vspider')
        self.cursor = self.db.cursor()
    def process_item(self,item,spider):
        #insert sql
        insert_sql = 'insert into dm_vdinfo (name,image_url,page_url,iframe_url,m3u8_url) values (%s,%s,%s,%s,%s)'
        data = dict(item)
        try:
            self.cursor.execute(insert_sql,(data['name'],data['image_url'],data['page_url'],data['iframe_url'],data['m3u8_url']))
            self.db.commit()
        except Exception as e:
            print(e)
            pass
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()


class S1482Pipeline:


    def __init__(self):
        self.db = pymysql.connect('192.168.10.100', 'root', 'pp123', 'vspider')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        print(item)
        # insert sql
        insert_sql = 'insert into om_2_moive (name,image_url,page_url,iframe_url,m3u8_url) values (%s,%s,%s,%s,%s)'
        data = dict(item)
        try:
            self.cursor.execute(insert_sql, (data['name'], data['image_url'], data['page_url'], data['iframe_url'], data['m3u8_url']))
            self.db.commit()
        except Exception as e:
            print(e)
            pass
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

