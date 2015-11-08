import cortipy
import os
import mysql.connector as msc
import time
import sys
from textblob import TextBlob
import json

apiKey = os.environ.get('CORTICAL_API_KEY')
MYSQL_GSA_PASSWORD = os.environ.get('MYSQL_GSA_PASSWORD')
client = cortipy.CorticalClient(apiKey)

config = {
   'user': 'root',
   'password': MYSQL_GSA_PASSWORD,
   'host': '130.211.154.93',
   'database': 'test',
   'charset': 'utf8'
}

#print "usage = python ClassifyVCs.py vctest4 (VC scraper) -or- python ClassifyVCs.py crunchbase_startups (startup capital scraper)"

dbtable = "crunchbase_startups"
dbtable = sys.argv[1]
#print "dbtable = " + dbtable

#Need to put this into an infinite loop
# while 1:
con = msc.connect(**config)
cur = con.cursor()
cur.execute("select siteurl, market, funding_total_usd, status, country_code, state_code, funding_rounds, cortical_io, watson, opencalais, cortical_io_keywords from "+dbtable+" where cortical_io is not null and text <> ''")
full = cur.fetchall()

#top 12 categories by funding raised in USD
categories = ("Biotechnology", "Communities", "Clean Technology", "Curated Web", "Consumer Electronics", "Advertising", "Analytics", "Batteries", "Clinical Trials", "Big Data", "Banking")

# build positive examples
i = 0
cur = con.cursor()
cur.execute("select siteurl, text from "+dbtable+" where cortical_io is not null and text <> '' and market = '"+categories[i]+"' and status='operating' and country_code = 'USA' and funding_rounds>0 ORDER BY RAND() limit 1;")
pos = cur.fetchall()
postext = []
for i in range(0, len(pos)):
    postext.append(pos[i][1])

# build negative examples
cur = con.cursor()
cur.execute("select siteurl, text from "+dbtable+" where cortical_io is not null and text <> '' and market <> '"+categories[i]+"' and status='operating' and country_code = 'USA' and funding_rounds>0 ORDER BY RAND() limit 1;")
neg = cur.fetchall()
negtext = []
for i in range(0, len(neg)):
    negtext.append(neg[i][1])

#build classifier based on pos text
CBCategoryClassifier = client.createClassification("test", postext, "")

# Chcek Term similarity
#unseenTermBitmap = client.getBitmap(categories[i])['fingerprint']['positions']
for i in range(0, len(categories)):
    unseenTermBitmap = client.getTextBitmap(categories[i])['fingerprint']['positions']
    distances = client.compare(unseenTermBitmap, CBCategoryClassifier['positions'])
    print categories[i] + " " + str(distances['euclideanDistance'])

pos[0][0]

print distances['euclideanDistance']

#check new copy
unseenBitmap = client.getTextBitmap("The Zen of Python >>>import this")['fingerprint']['positions']
distances = client.compare(unseenBitmap, CBCategoryClassifier['positions'])
print distances['euclideanDistance']


for i in range(0, len(full)):
    siteurl[i] = str(full[i][0])
    market[i] = str(full[i][1])
    funding[i] = str(full[i][2])
    status[i] = str(full[i][3])
    country[i] = str(full[i][4])
    state[i] = str(full[i][5])
    funding[i] = str(full[i][6])
    cortical_io[i] = json.loads(full[i][7])
    watson[i] = str(full[i][8])
    opencalais[i] = str(full[i][9])
    keywords[i] = str(full[i][10])

    #Cortical.io
    termKeyWords = client.extractKeywords(text)
    termBitmap = client.getTextBitmap(text)['fingerprint']['positions']

    #TextBlob
    blob = TextBlob(text)

    MySqlKeyWordDat = (','.join(termKeyWords), siteurl)
    MySqlBitMapDat = (str(termBitmap), siteurl)
    MySqlTextBlobDat = (str(blob.sentiment), siteurl)
    MySqLangDat = (str(blob.detect_language()), siteurl)

    print "---For "+siteurl+" keywords = " + ",".join(termKeyWords) + " sentiment = " + MySqlTextBlobDat[0] + " lang:" + MySqLangDat[0]

    MySqlKeyWordDatQ = """UPDATE """+dbtable+""" SET cortical_io_keywords = %s WHERE siteurl = %s"""
    MySqlBitMapDatQ = """UPDATE """+dbtable+""" SET cortical_io = %s WHERE siteurl = %s"""
    MySqBlobDatQ = """UPDATE """+dbtable+""" SET opencalais = %s WHERE siteurl = %s"""
    MySqLangDatQ = """UPDATE """+dbtable+""" SET watson = %s WHERE siteurl = %s"""

    #upload keywords and bitmap to database
    cur.execute(MySqlKeyWordDatQ, MySqlKeyWordDat)
    cur.execute(MySqlBitMapDatQ, MySqlBitMapDat)
    cur.execute(MySqBlobDatQ, MySqlTextBlobDat)
    cur.execute(MySqLangDatQ, MySqLangDat)
    con.commit()

#programmingCategory = client.createClassification(categoryName, pos, neg)
#if(text == ''):
#    continue

con.close()

#bitmapTerms = client.bitmapToTerms(termBitmap['fingerprint'])






######  sample code bleow.
# Evaluate how close a new term is to the category.
#termBitmap = client.getBitmap("Python")['fingerprint']['positions']
#distances = client.compare(termBitmap, programmingCategory['positions'])
#print distances['euclideanDistance']

# Try a block of text.
#textBitmap = client.getTextBitmap("The Zen of Python >>>import this")['fingerprint']['positions']
#distances = client.compare(textBitmap, programmingCategory['positions'])
#print distances['euclideanDistance']
