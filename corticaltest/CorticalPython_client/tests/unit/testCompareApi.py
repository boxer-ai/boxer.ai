# -*- coding: utf-8 -*-
"""
/*******************************************************************************
 * Copyright (c) cortical.io GmbH. All rights reserved.
 *  
 * This software is confidential and proprietary information.
 * You shall use it only in accordance with the terms of the
 * license agreement you entered into with cortical.io GmbH.
 ******************************************************************************/
"""
import unittest

from cortical.compareApi import CompareApi

import testConfiguration


inputJSONarray = '[ { "term" : "apple" }, { "text" : "banana is a kind of fruit" } ]'
bulkJSONarray = '[ [ { "term" : "jaguar" }, { "term" : "car" } ], [ { "term" : "jaguar" }, { "term" : "cat" } ] ]'
oneTermInputJSONarray = "[ { \"term\" : \"apple\" } ]"
syntaxErrorJSONarray = "[ { \"term\" : \"apple\" }, { \"term\" : \"banana\"  ]"

class TestClientCompareApi(unittest.TestCase):
 

    def setUp(self):
        self.compareApi = CompareApi(testConfiguration.client)

    def testCompare(self):
        resultMetric = self.compareApi.compare(testConfiguration.RETINA_NAME, inputJSONarray)
        self.assertGreater(resultMetric.cosineSimilarity, 0.1)
        self.assertGreater(resultMetric.euclideanDistance, 0.1)
        self.assertGreater(resultMetric.jaccardDistance, 0.1)
        self.assertGreater(resultMetric.weightedScoring, 0.1)
        self.assertGreater(resultMetric.sizeRight, 10)
        self.assertGreater(resultMetric.sizeLeft, 10)
        self.assertGreater(resultMetric.overlappingLeftRight, 0.1)
        self.assertGreater(resultMetric.overlappingAll, 10)
        self.assertGreater(resultMetric.overlappingRightLeft, 0.1)

    def testCompareBulk(self):
        resultMetricList = self.compareApi.compareBulk(testConfiguration.RETINA_NAME, bulkJSONarray)
        self.assertEqual(len(resultMetricList), 2)
        for resultMetric in resultMetricList:
            self.assertGreater(resultMetric.cosineSimilarity, 0.1)
            self.assertGreater(resultMetric.euclideanDistance, 0.1)
            self.assertGreater(resultMetric.jaccardDistance, 0.1)
            self.assertGreater(resultMetric.weightedScoring, 0.1)
            self.assertGreater(resultMetric.sizeRight, 10)
            self.assertGreater(resultMetric.sizeLeft, 10)
            self.assertGreater(resultMetric.overlappingLeftRight, 0.1)
            self.assertGreater(resultMetric.overlappingAll, 10)
            self.assertGreater(resultMetric.overlappingRightLeft, 0.1)
        

    def testException(self):
        # testing using only one input element in the array
        expectedException = False
        try:
            self.compareApi.compare(testConfiguration.RETINA_NAME, oneTermInputJSONarray)
        except Exception:
            expectedException = True
        self.assertTrue(expectedException)
        
        # testing JSON parse exception in the input
        expectedException = False
        try:
            self.compareApi.compare(testConfiguration.RETINA_NAME, syntaxErrorJSONarray)
        except Exception:
            expectedException = True
        self.assertTrue(expectedException)


if __name__ == "__main__":
    unittest.main()


