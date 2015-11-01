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

from cortical.imageApi import ImageApi

import testConfiguration

inputJSON = '{ "term" : "apple" }'
inputJSONarray = '[ { "term" : "apple" }, { "term" : "banana" } ]'
inputJSONarray3 = '[ { "term" : "apple" }, { "term" : "banana" }, { "term" : "fruit" } ]'

class TestClientImageApi(unittest.TestCase):
    
    def setUp(self):
        self.api = ImageApi(testConfiguration.client)


    def testImage(self):
        imageData = self.api.getImageForExpression(testConfiguration.RETINA_NAME, inputJSON)
        self.assertNotEqual(imageData, None)

    def testCompare(self):
        imageData = self.api.getOverlayImage(testConfiguration.RETINA_NAME, inputJSONarray)
        self.assertNotEqual(imageData, None)

    def testBulk(self):
        images = self.api.getImageForBulkExpressions(testConfiguration.RETINA_NAME, inputJSONarray3, get_fingerprint=True)
        self.assertEqual(len(images), 3)
        for image in images:
            self.assertNotEqual(image, None)
            self.assertNotEqual(image.image_data, None)
            self.assertNotEqual(len(image.fingerprint.positions), 0)

if __name__ == "__main__":
    unittest.main()
