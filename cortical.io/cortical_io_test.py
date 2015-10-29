from cortical.client import ApiClient
from cortical.termsApi import TermsApi

client = ApiClient(apiKey="fa786e60-7cf0-11e5-9e69-03c0722e0d16", apiServer="http://api.cortical.io/rest")
api = TermsApi(client)
terms = api.getTerm("en_associative", term="apple", get_fingerprint=True)

print terms[0].fingerprint.positions

