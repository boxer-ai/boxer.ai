'''
Created on May 4, 2015

@author: soren
'''
from cortical.classifyApi import ClassifyApi

import testConfiguration
import unittest

filterInput1 = \
"""{
 "positiveExamples" : [
     { "text" : "Shoe with a lining to help keep your feet dry and comfortable on wet terrain." },
     { "text" : "running shoes providing protective cushioning." }
                     ],
"negativeExamples" : [ 
     { "text" : "The most comfortable socks for your feet."}, 
     { "text" : "6 feet USB cable basic white"}
                     ]
}
"""

class TestClassifyApi(unittest.TestCase):


    def setUp(self):
        self.classifyApi = ClassifyApi(testConfiguration.client)

    def testCreateCategoryFilter(self):
        filterName = "filter1"
        filter1 = self.classifyApi.createCategoryFilter(testConfiguration.RETINA_NAME, filterName, filterInput1)
        self.assertGreater(len(filter1.positions), 50)
        self.assertEqual(filter1.categoryName, filterName)
        
    def testErrors(self):
        expectedException = False
        try:
            self.classifyApi.createCategoryFilter(testConfiguration.RETINA_NAME, None, filterInput1)
        except Exception:
            expectedException = True
        self.assertTrue(expectedException)
        
        expectedException = False
        try:
            self.classifyApi.createCategoryFilter(testConfiguration.RETINA_NAME, "Filter", 
                                                  '"negativeExamples" : [{ "text" : "cable"} ]')
        except Exception, e:
            expectedException = True
        self.assertTrue(expectedException)


if __name__ == "__main__":
    unittest.main()