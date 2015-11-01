
import json
from collections import defaultdict
from client import CorticalClient
import random

# Put your cortical.io API key in a file with this name
corticalio_keyfile = "cortical.io.key"
corticalio_key = open("cortical.io.key").readline()
corticalio_key = corticalio_key.replace("YOUR KEY: ", "").replace("\n", "")

# Download and unzip Yelp's academic dataset so you have this file
yelp_dataset = 'yelp_academic_dataset.json'

# Number of users to analyze
num_users = 100

################################################################################
# Parse Yelp academic dataset
################################################################################

reviews_by_biz = defaultdict(list)
reviews_by_user = defaultdict(list)
bizs = {}
users = {}

with open(yelp_dataset) as f:
    for l in f:
        parsed = json.loads(l)
        type = parsed['type']
        if type == 'user':
            users[parsed['user_id']] = parsed
        elif type == 'business':
            bizs[parsed['business_id']] = parsed
        elif type == 'review':
            reviews_by_biz[parsed['business_id']].append(parsed)
            reviews_by_user[parsed['user_id']].append(parsed)
        else:
            print parsed

print "Number of businesses:", len(bizs)
print "Number of users:", len(users)

################################################################################
# Use Cortical IO to analyze dataset
################################################################################
client = CorticalClient(corticalio_key, apiServer="http://s_api.cortical.io:80", retinaName="en_synonymous")

reviews_per_user = {}
terms = {}
total_reviews = 0
for i in range(num_users):
    user = random.choice(users.keys())
    # Build histogram of # reviews per user
    print "User #:", i + 1
    print "User ID:", user
    total_reviews = total_reviews + len(reviews_by_user[user])

    # Build a sorted list of terms
    for review in reviews_by_user[user]:
        text_response = client.text(review['text'].encode('utf-8'))
        if text_response:
            sdr = text_response[0]['positions']
            review_terms = client.getSimilarTermsForSDR(sdr, 1)
            print review_terms
            for term in review_terms:
                if term in terms:
                    terms[term] = terms[term] + 1
                else:
                    terms[term] = 1
    print


print "Number of reviews analyzed:", total_reviews

sorted_terms = sorted(terms, key=lambda term: terms[term])

print "Term most closely associated with review, number of reviews"
for term in sorted_terms:
    print term + ",", terms[term]
