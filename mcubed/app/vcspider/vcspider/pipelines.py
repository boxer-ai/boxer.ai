import json
import mysql.connector as msc
from scrapy.conf import settings
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from collections import defaultdict

class UserInputPipeline(object):

    def __init__(self):
        self.sitetext = defaultdict(str)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        # gotta grab these from environ/settings
        config =  {
            'user': 'root',
            'password': 'uLFZ2WoB',
            'host': '130.211.154.93',
            'database': 'test'
        }
        self.MYSQL_TABLE_SU = 'crunchbase_startups'

        self.con = msc.connect(**config)
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        dc = dict(item)
        for key in dc.keys():  # strip out bs list structure
            dc[key] = ''.join(dc[key])

        # appending site text as you scrape
        self.sitetext[dc['siteurl']] += ' {}'.format(dc['text'])

        return

    def spider_closed(self, spider):
        sitekv = [(v,k) for k,v in self.sitetext.items()]
        sql = self.get_insert_query().format(self.MYSQL_TABLE_SU)
        self.cur.execute(sql, sitekv[0]) # keeping tuple comprehension for if i do multiple sites
        self.con.commit()

        self.con.close()

        return

    def get_insert_query(self):
        return 'INSERT INTO {0} (text, siteurl) VALUES (%s, %s);'


class MySqlPipeline(object):

    def __init__(self):

        config = settings['MYSQL_GSA_CONFIG']
        self.con = msc.connect(**config)
        self.cur = self.con.cursor()

        self.sitekeys = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):

        dc = dict(item) # old way to do it
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

    def build_text(self, dc): # this is not needed if you use defaultdicts

        if dc['siteurl'] not in self.sitekeys:
            self.sitekeys[dc['siteurl']] = dc['text']

        elif dc['siteurl'] in self.sitekeys:
            self.sitekeys[dc['siteurl']] += dc['text']


    def get_update_query(self):
        return "UPDATE {0} SET text = concat(ifnull(text, ''), %s) WHERE siteurl LIKE %s;"

    def get_insert_query(self):
        return "INSERT INTO {0} (text, siteurl) VALUES (%s, %s);"
