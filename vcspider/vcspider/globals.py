import pandas as pd
import re
# import os

# print os.getcwd()
vcsites = pd.read_csv('/Users/avi/programming/banker.ai/vcspider/private_funds.csv', sep='|')

domains = vcsites.Web.dropna()
domains = domains.apply(lambda x: re.sub(r'((http(s)?://)?(www.)?)', '', x.lower())).tolist()
urls = map(lambda domain: 'http://www.' + domain, domains)
