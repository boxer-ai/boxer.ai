# from cortical.client import ApiClient
# from cortical.termsApi import TermsApi

# client = ApiClient(apiKey="fa786e60-7cf0-11e5-9e69-03c0722e0d16", apiServer="http://api.cortical.io/rest")
# api = TermsApi(client)
# terms = api.getTerm("en_associative", term="apple", get_fingerprint=True)

# print terms[0].fingerprint.positions


import cortipy
import os

# Init API client
apiKey = os.environ.get('CORTICAL_API_KEY')
client = cortipy.CorticalClient(apiKey)

# Create the category with some positive (and negative) examples, and a name.
pos = [
    "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.",
    "To iterate is human, to recurse divine.",
    "First learn computer science and all the theory. Next develop a programming style. Then forget all that and just hack."
    ]
neg = [
    "To err is human, to forgive divine."
    ]
categoryName = "programming quotes"
programmingCategory = client.createClassification(categoryName, pos, neg)

# Evaluate how close a new term is to the category.
termBitmap = client.getBitmap("Python")['fingerprint']['positions']
distances = client.compare(termBitmap, programmingCategory['positions'])
print distances['euclideanDistance']

# Try a block of text.
textBitmap = client.getTextBitmap("The Zen of Python >>>import this")['fingerprint']['positions']
distances = client.compare(textBitmap, programmingCategory['positions'])
print distances['euclideanDistance']

file_name = "15_UTX.txt"
with open('Company_Descriptions/'+file_name, "r") as myfile:
    body = myfile.read().replace('\n', '')

# Chose either en_synonymous or en_associative retina
text = TextApi(client).getRepresentationForText("en_synonymous", body)
print text[0].positions
