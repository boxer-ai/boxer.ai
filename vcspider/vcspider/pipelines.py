import json
import mysql.connector as msc
from scrapy.conf import settings
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


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

        self.sitekeys = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):

        dc = dict(item)
        for key in dc.keys():  # strip out bs list structure
            dc[key] = ''.join(dc[key])
        self.build_text(dc)

        return

    def spider_closed(self, spider):

        sql = self.get_update_query()
        sql = sql.format(settings['MYSQL_TABLE_VC']) if spider.name == 'vcs' else sql.format(settings['MYSQL_TABLE_SU'])

        sitekv = [(v,k) for k,v in self.sitekeys.iteritems()]

        self.cur.executemany(sql, sitekv)
        self.con.commit()

        self.con.close()

    def build_text(self, dc):

        if dc['siteurl'] not in self.sitekeys:
            self.sitekeys[dc['siteurl']] = dc['text']

        elif dc['siteurl'] in self.sitekeys:
            self.sitekeys[dc['siteurl']] += dc['text']


    def get_update_query(self):
        return "UPDATE {0} SET text = concat(ifnull(text, ''), %s) WHERE siteurl LIKE %s;"

    def get_insert_query(self):
        return "INSERT INTO {0} (text, siteurl) VALUES (%s, %s);"
