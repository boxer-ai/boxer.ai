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
        self.sitekeys = []

    def process_item(self, item, spider):

        dc = dict(item)
        for key in dc.keys():  # strip out bs list structure
            dc[key] = ''.join(dc[key])

        sql = self.get_update_query() #if self.check_key(item) else self.get_insert_query()
        sql = sql.format(settings['MYSQL_TABLE_VC']) if spider.name == 'vcs' else sql.format(settings['MYSQL_TABLE_SU'])
        # print dc['text'], dc['siteurl']
        # print sql, 'post'
        # print dc['siteurl']

        self.cur.execute(sql, dc)
        self.con.commit()

        return

    def spider_closed(self, spider):
        self.con.close()

    def check_key(self, item):
        if item['siteurl'] not in self.sitekeys:
            self.sitekeys.append(item['siteurl'])
            return False

        elif item['siteurl'] in self.sitekeys:
            return True

    def get_update_query(self):
        return "UPDATE {0} SET text = concat(text, %(text)s) WHERE siteurl LIKE %(siteurl)s;"

    def get_insert_query(self):
        return "INSERT INTO {0} (text, siteurl) VALUES (%(text)s, %(siteurl)s);"
