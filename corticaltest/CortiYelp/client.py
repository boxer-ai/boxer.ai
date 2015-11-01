import json
import urllib
import urllib2


class CorticalClient(object):
    """
    This class implements some basic access to Cortical.io's retina.
    Please have a look at api.cortical.io to see the full array of REST endpoints, and input and output types.
    The naming conventions of the methods are heavily related to the names of the rest endpoints.
    """

    def __init__(self, apiKey, apiServer="http://s_api.cortical.io:80", retinaName="en_synonymous"):
        """
        retinaName: one of: 'en_synonymous', 'en_associative'
        """
        apiWeb = "http://www.cortical.io/developers_apikey.html"
        if apiKey is None:
            raise Exception('You must pass an apiKey when instantiating the APIClient. Get one here: %s' % (str(apiWeb)))
        self.apiKey = apiKey
        self.apiServer = apiServer
        self.retinaName = retinaName


# some handy short cuts ####

    def getSimilarTermsForSDR(self, sdr, howMany):
        """sdr is a numpy.ndarray. Returns a list of terms"""
        expression = '{ "positions" : [%s] }' % (",".join([str(val) for val in sdr]))
        fpList = self.expressions_similar_terms(expression, start_index=0, max_results=howMany, get_fingerprint=True)
        return [d['term'] for d in fpList]



# rest calls ####

    def terms(self, term, start_index=0, max_results=10, get_fingerprint=True):
        """Get a Term object for the input term"""
        resourcePath = "/rest/terms?retina_name=%s&term=%s&start_index=%i&max_results=%i&get_fingerprint=%s" \
            % (self.retinaName, urllib.quote(term), start_index, max_results, get_fingerprint)
        res = None
        try:
            res = self._callAPI(resourcePath, "GET", None)
        except Exception, e:
            print "Failed calling with term " + term + "\n"
            print e
        return res

    def terms_similar_terms(self, term, context_id=None, start_index=0, max_results=10, pos_type="", get_fingerprint=False):
        """Get similar terms for a term"""
        resourcePath = "/rest/terms/similar_terms?retina_name=%s&term=%s&start_index=%i&max_results=%i&get_fingerprint=%s" \
            % (self.retinaName, urllib.quote(term), start_index, max_results, get_fingerprint)
        if pos_type:
            resourcePath += "&pos_type=%s" % (pos_type)
        if type(context_id) == int:
            resourcePath += "&context_id=%i" % (context_id)
        res = None
        try:
            res = self._callAPI(resourcePath, "GET", None)
        except Exception, e:
            print e
        return res

    def text(self, inputText):
        """Get SDR for a text"""
        resourcePath = "/rest/text?retina_name=%s" % (self.retinaName)
        res = None
        try:
            res = self._callAPI(resourcePath, "POST", inputText)
        except Exception, e:
            print e
        return res

    def text_keywords(self, inputText):
        """ Calls the getKeyords for text endpoint of the Cortical API."""
        resourcePath = "/rest/text/keywords?retina_name=%s" % (self.retinaName)
        res = None
        try:
            res = self._callAPI(resourcePath, "POST", inputText)
        except Exception, e:
            print e
        return res

    def text_slices(self, inputText, startIndex=0, maxResults=10, getFingerprint=False):
        """ Calls the get slices for text endpoint of the Cortical API."""
        resourcePath = "/rest/text/slices?retina_name=%s&start_index=%i&max_results=%i&get_fingerprint=%s" \
            % (self.retinaName, startIndex, maxResults, getFingerprint)

        slices = None
        try:
            slices = self._callAPI(resourcePath, "POST", inputText)
        except Exception, e:
            print e
        return slices

    def text_tokenize(self, inputText, posTags=None):
        """Get sentences and tokens for a text"""
        resourcePath = "/rest/text/tokenize?retina_name=%s" % (self.retinaName)

        if posTags:
            resourcePath += "&POStags=%s" % (urllib.quote(posTags))
        res = None
        try:
            res = self._callAPI(resourcePath, "POST", inputText)
        except Exception, e:
            print e
        return res

    def expressions_similar_terms(self, expression, context_id=None, start_index=0, max_results=10, pos_type="", sparsity=1.0, get_fingerprint=False):
        """Get similar terms for an expression"""
        resourcePath = "/rest/expressions/similar_terms?retina_name=%s&start_index=%i&max_results=%i&sparsity=%f&get_fingerprint=%s" \
            % (self.retinaName, start_index, max_results, sparsity, get_fingerprint)
        if pos_type:
            resourcePath += "&pos_type=%s" % (pos_type)
        if type(context_id) == int:
            resourcePath += "&context_id=%i" % (context_id)
        res = None
        try:
            res = self._callAPI(resourcePath, "POST", expression)
        except Exception, e:
            print e
        return res

    def compare(self, fingerprint1, fingerprint2):
        resourcePath = "/rest/compare?retina_name=%s" % (self.retinaName)

        expression = ""
        if (fingerprint1 and fingerprint2):
            expression = "[ { \"positions\":" + str(fingerprint1) + "} , { \"positions\":" + str(fingerprint2) + " } ]"

        res = None
        try:
            res = self._callAPI(resourcePath, "POST", expression)
        except Exception, e:
            print e
        return res

    def _callAPI(self, resourcePath, method, postData):

        url = self.apiServer + resourcePath
        data = postData
        headers = {}
        headers['api-key'] = self.apiKey

        # print "url", url
        headers['api-key'] = '58baa020-97b4-11e3-82ec-614a46604ad2'

        if method in ['GET']:
            pass
        elif method in ['POST', 'PUT', 'DELETE']:
            if postData:
                headers['Content-type'] = 'application/json'
        else:
            raise Exception('Method ' + method + ' is not recognized.')

        request = urllib2.Request(url=url.encode('utf-8'), headers=headers, data=data)
        response = urllib2.urlopen(request)
        string = response.read()

        try:
            data = json.loads(string)
        except ValueError:
            data = None

        return data
