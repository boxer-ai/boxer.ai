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

from cortical.termsApi import TermsApi

import testConfiguration

class TestClientTermsApi(unittest.TestCase):
    
    def setUp(self):
        self.termsApi = TermsApi(testConfiguration.client)

    def testOneException(self):
        exceptionOccurred = False
        try:
            self.termsApi.getTerm("not_retina_name", term="apple", get_fingerprint=True, start_index=0, max_results=5)
        except Exception:
            exceptionOccurred = True
        self.assertTrue(exceptionOccurred)

    def testTerms(self):
        terms = self.termsApi.getTerm(testConfiguration.RETINA_NAME, term="apple", get_fingerprint=True, start_index=0, max_results=5)
        self.assertFalse(terms == None)
        self.assertTrue(len(terms) == 1)
        self.assertTrue(terms[0].term == "apple")
        self.assertTrue("NOUN" in terms[0].pos_types)
        self.assertTrue(terms[0].df > 0.0001)
        self.assertGreater(len(terms[0].fingerprint.positions), 100)

    def testContexts(self):
        contexts = self.termsApi.getContextsForTerm(testConfiguration.RETINA_NAME, term="apple", get_fingerprint=True, start_index=0, max_results=3)
        self.assertTrue(contexts != None)
        self.assertEqual(3, len(contexts))
        c0 = contexts[0]
        self.assertGreater(len(c0.fingerprint.positions), 100)
        self.assertTrue(isinstance(c0.context_label, unicode))
        self.assertTrue(c0.context_id == 0)

    def testSimilarTerms(self):
        terms = self.termsApi.getSimilarTerms(testConfiguration.RETINA_NAME, term="apple", context_id=0, pos_type="NOUN", get_fingerprint=True, start_index=0, max_results=8)
        self.assertTrue(terms != None)
        self.assertEqual(8, len(terms))
        t0 = terms[0]
        self.assertTrue(len(t0.fingerprint.positions) > 0)
        self.assertTrue(t0 != None)

    def testExceptionTerms(self):
        exceptionOccurred = False
        try:
            terms = self.termsApi.getSimilarTerms(testConfiguration.RETINA_NAME, term="apple", context_id=0, pos_type="wrong", get_fingerprint=True, start_index=0, max_results=8)
        except Exception, ex:
            exceptionOccurred = True
        self.assertTrue(exceptionOccurred)
        
if __name__ == "__main__":
    unittest.main()
