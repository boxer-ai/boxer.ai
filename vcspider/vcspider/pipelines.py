import json
import mysql.connector as msc
from scrapy.conf import settings


class VcspiderPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySqlPipeline(object):

    def __init__(self):

        config = settings['MYSQL_GSA_CONFIG']
        self.con = msc.connect(**config)
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        dc = dict(item)
        dclist = []

        for val in dc.values():
            dclist.append(''.join(val).encode('utf-8'))

        values = '\', \''.join(dclist)

        sql = "INSERT INTO vctest (pagetitle, text, pageurl, siteurl) VALUES ('{0}');".format(values)

        self.cur.execute(sql)
        self.con.commit()

        return

    def spider_closed(self, spider):
        self.con.close()
