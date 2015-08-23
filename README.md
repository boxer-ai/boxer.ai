# Semantic fingerprinting with company descriptions

To obtain semantic fingerprints of companies we must use the Cortical API.

One can interact with the API in various ways. You can use the web client or a local client. For the purposes of this paper we used a local client. Cortical have local clients for the Java, PHP, and Python programming languages however due to our familiarity with the Python programming language we’ve chosen to use the Python client. You can download a folder with the files and scripts used in this research paper.

###	Tools

The tools used for this project were:

*	Cortical API (2.2.0)
*	Cortical API key
*	Python 2.7 with Requests extension (Anaconda Python distribution)
*	Cortical Python client (v2.2.0)
*	Statistical analysis software


###	Method and code

The code in this repository will generate a list of keywords, a fingerprint vector, and a fingerprint image generated for a given text.

The python script will only run if you add your cortical API key to the apiKey variable on line 18.

Furthermore on line 26 of GenerateFingerprint.py you can change which company description is analysed from the /Company_Descriptions directory.

The script will generate a semantic fingerprint vector, a keywords list, and an image of the fingerprint (in this order). It will generate these for the text (string) written in the body variable on line 20.
