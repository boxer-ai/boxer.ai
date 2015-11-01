####################################################
################### Setup code #####################
####################################################
import os
# Adding cortical client to Python path
import sys
#client_path = '%s/CorticalPython_client/' % os.path.dirname(os.path.realpath(__file__))
client_path = '%s/CorticalPython_client/' % os.path.dirname(os.path.realpath("GenerateFingerprint.py"))

sys.path.append(client_path)

# Importing cortical API to script
from cortical.client import ApiClient

#import TextApi for fingerprint vector and keywords
from cortical.textApi import TextApi

#import ImageApi for generating fingerprint image
from cortical.imageApi import ImageApi

corticalio_key = open("cortical.io.key").readline()
corticalio_key = corticalio_key.replace("YOUR KEY: ", "").replace("\n", "")

client = ApiClient(apiKey=corticalio_key, apiServer="http://api.cortical.io/rest")

# Body contains string of text to be analysed

# Code to get fingerprints from a string
# Body = "Semantic fingerprints are cool."

# Code to get fingerprints from a .txt file put filename
file_name = "15_AA.txt"

with open('Company_Descriptions/'+file_name, "r") as myfile:
    body = myfile.read().replace('\n', '')

####################################################
######### Code for fingerprint (vector) ############
####################################################

# Chose either en_synonymous or en_associative retina
text = TextApi(client).getRepresentationForText("en_synonymous", body)
print text[0].positions

####################################################
############# Code for keywords list ###############
####################################################

# Chose either en_synonymous or en_associative retina
terms = TextApi(client).getKeywordsForText("en_synonymous", body)
print terms

#####################################################
########## Code for fingerprint (image) #############
#####################################################

body = '{"text":"%s"}' % body

# Chose either en_synonymous or en_associative (default) retina, image scalar (default: 2), square or circle (default) image, encoding type, and sparsity
terms = ImageApi(client).getImageForExpression("en_synonymous", body, 2, "square", "base64/png", '1.0')

# Chose image name
image_name = file_name.replace(".txt", "")
fh = open(image_name + "_fpImage.png", "wb")
fh.write(terms.decode('base64'))
fh.close()
print(image_name + ' fingerprint image saved to %s') % os.path.dirname(os.path.realpath(__file__))

#####################################################
################## End of Script ####################
#####################################################
