import pandas as pd
import re
# import os

# print os.getcwd()
vcsites = pd.read_csv('private_funds.csv', sep='|')
susites = pd.read_csv('startups.csv')

domains = vcsites.Web.dropna()
domains = domains.apply(lambda x: re.sub(r'((http(s)?://)?(www.)?)', '', x.lower())).tolist()
urls = map(lambda domain: 'http://www.' + domain, domains)

domains_su = susites.domains.dropna()
domains_su = domains_su.apply(lambda x: re.sub(r'((http(s)?://)?(www.)?)', '', x.lower())).tolist()
urls_su = map(lambda domain: 'http://www.' + domain, domains_su)
