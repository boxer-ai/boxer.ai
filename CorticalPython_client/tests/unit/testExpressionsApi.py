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

from cortical.expressionsApi import ExpressionsApi

import testConfiguration as conf

oneTermInputJSON = '{ "term" : "apple" }'

class TestClientExpreissions(unittest.TestCase):
    

    def setUp(self):
        self.api = ExpressionsApi(conf.client)
        self.jsonBulkExpression = None
        # path relative to current working dir
        with open("bulkInput.json", "r") as f:
            self.jsonBulkExpression = "".join(f.readlines())
        
    def testExpressions(self):
        fp = self.api.resolveExpression(conf.RETINA_NAME, oneTermInputJSON, sparsity=0.5)
        self.assertGreater(len(fp.positions), 100)

    def testContexts(self):
        contexts = self.api.getContextsForExpression(conf.RETINA_NAME, oneTermInputJSON, get_fingerprint=True, start_index=0, max_results=3, sparsity=1.0)
        self.assertTrue(contexts != None)
        self.assertEqual(3, len(contexts))
        c0 = contexts[0]
        self.assertGreater(len(c0.fingerprint.positions), 100)
        self.assertTrue(isinstance(c0.context_label, unicode))
        self.assertTrue(c0.context_id == 0)

    def testSimilarTerms(self):
        terms = self.api.getSimilarTermsForExpressionContext(conf.RETINA_NAME, oneTermInputJSON, context_id=None, pos_type="NOUN", get_fingerprint=True, start_index=0, max_results=8, sparsity=1.0)
        self.assertTrue(terms != None)
        self.assertEqual(8, len(terms))
        t0 = terms[0]
        self.assertGreater(len(t0.fingerprint.positions), 100)
        self.assertTrue(t0 != None)

    def testExpressionBulk(self):
        fps = self.api.resolveBulkExpression(conf.RETINA_NAME, self.jsonBulkExpression)
        self.assertEqual(6, len(fps))
        for fp in fps:
            self.assertGreater(len(fp.positions), 50)

    def testExpressionContextsBulk(self):
        contextsList = self.api.getContextsForBulkExpression(conf.RETINA_NAME, self.jsonBulkExpression, get_fingerprint=True, start_index=0, max_results=3)
        self.assertEqual(len(contextsList), 6)
        for contextList in contextsList:
            for i, context in enumerate(contextList):
                self.assertGreater(len(context.fingerprint.positions), 50)
                self.assertTrue(isinstance(context.context_label, unicode))
                self.assertTrue(context.context_id == i)

    def testExpressionSimilarTermsBulk(self):
        termsLists = self.api.getSimilarTermsForBulkExpressionContext(conf.RETINA_NAME, self.jsonBulkExpression, get_fingerprint=True, max_results=7)
        self.assertTrue(len(termsLists) == 6)
        for termList in termsLists:
            self.assertTrue(len(termList) == 7)
            self.assertGreater(len(termList[0].fingerprint.positions), 100)

if __name__ == "__main__":
    unittest.main()

