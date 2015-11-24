import cortipy
import mysql.connector as msc
from collections import namedtuple, defaultdict
from gensim import corpora, models, similarities
from app.vcspider.vcspider.settings import MYSQL_GSA_CONFIG, CORTIPY_API_KEY
# import sqlalchemy
# apiKey = os.environ.get('CORTICAL_API_KEY')
# MYSQL_GSA_PASSWORD = os.environ.get('MYSQL_GSA_PASSWORD')

client = cortipy.CorticalClient(CORTIPY_API_KEY)

con = msc.connect(**MYSQL_GSA_CONFIG)
cur = con.cursor()

stoplist = set('for a of the and to in on from'.split())
CSite = namedtuple('CorticalSite', 'siteurl text fingerprint keywords')

def getSDR(sitetype):
    sql_getsite = "SELECT siteurl, text FROM %s WHERE NULLIF(text, '') IS NOT NULL ORDER BY RAND() LIMIT 1;"
    cur.execute(sql_getsite % sitetype)
    siteurl, text = cur.fetchone()

    site_corticalmap = client.createClassification(siteurl, [text], "")
    site_keywords = client.extractKeywords(text)

    return CSite(siteurl, text, site_corticalmap['positions'], [site_keywords])

def getSDRDist(site1, site2, metric = 'euclideanDistance'):
    print site1.fingerprint, site2.fingerprint
    return client.compare(site1.fingerprint, site2.fingerprint)[metric]


def gsClean(documents, freqLim = 5):
    frequency = defaultdict(int)

    if isinstance(documents, list): # multiple documents to clean
        texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
        for text in texts:
            for word in text:
                frequency[word] += 1

        texts = [[word for word in text if frequency[word] > freqLim] for text in texts]

    elif isinstance(documents, unicode): # only one
        texts = [word for word in documents.lower().split() if word not in stoplist]
        for word in texts:
            frequency[word] += 1

        texts = [word for word in texts if frequency[word] > freqLim]

    return texts


def gsMakeVectorsFromDocs(texts):
    gsDict = corpora.Dictionary(texts)
    gsDict.save('gsDict.dict')

    corpus = [gsDict.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('gsCorp.mm', corpus)


vcs, sus = list(), list()

for x in xrange(2):
    vcs.append(getSDR('vctest4'))
    sus.append(getSDR('crunchbase_startups'))



print



