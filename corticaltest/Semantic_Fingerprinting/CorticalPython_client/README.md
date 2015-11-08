cortical.io
===========
Welcome to the cortical.io Retina Python client source code page.

Release Version: 2.2.0

This page contains
<UL>
<LI><B>Introduction</B></LI>
<LI><B>Dependencies</B></LI>
<LI><B>How to use</B></LI>
<LI><B>Change Log</B></LI>
</UL>


### Introduction
cortical.io's Python client - a simple Python http client which simplifies the communication with the Retina server using the Retina's <a href="http://api.cortical.io/">REST API</a>. 
The source code is split into the following:

* `/cortical` Endpoint files - One for each endpoint group.
* `/cortical/models` - The return object classes.
* `/tests` - Unit tests of all endpoints and examples of their usage.


### Dependencies
cortical.io's Retina Python client has been tested with Python version 2.7 and with all 2.x.x versions of <a href="http://api.cortical.io">cortical.io's api</a>.

To use the API you will need to obtain an <a href="http://www.cortical.io/developers_apikey.html">api key</a>.


### How to use/build
* You will need Python (version 2.7 has been tested).
* Install the <a href="http://python-requests.org">Requests</a> library, for example using `pip install requests`.
* Clone all the sources from our Github repository.
* Add the location of the cloned repository to your PYTHONPATH

You should now be able to use the client in the following way (obtaining a sementic representation of the term *apple*):

```python
from cortical.client import ApiClient
from cortical.termsApi import TermsApi

client = ApiClient(apiKey="your_api_key", apiServer="http://api.cortical.io/rest")
api = TermsApi(client)
terms = api.getTerm("en_associative", term="apple", get_fingerprint=True)
print terms[0].fingerprint.positions
```

For further documentation about the Retina-API and information on cortical.io's 'Retina' technology please see: 
http://www.cortical.io/developers_tutorials.html. Also the `tests` folder contains more examples of how to use the client. 

If you have any questions or problems please visit our forum:
http://www.cortical.io/developers_forum.html

### Change Log
<B>v 2.2.0</B>
 * new Classfiy api with /classify/create_category_filter
 * new /text/detect_language endpoint
 * new /compare/bulk endpoint

<B>v 2.1.0</B>
* Initial release version.
