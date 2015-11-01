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

from cortical.retinasApi import RetinasApi

import testConfiguration


class TestClientRetinasApi(unittest.TestCase):
    

    def setUp(self):
        self.retinasApi = RetinasApi(testConfiguration.client);

    def testRetinas(self):
        
        retinas = self.retinasApi.getRetinas();
        self.assertNotEqual(retinas, None)
        self.assertNotEqual(retinas[0], None)
        self.assertNotEqual(retinas[1], None)
        self.assertTrue("en_synonymous" == retinas[0].retinaName or "en_associative" == retinas[0].retinaName)


if __name__ == "__main__":
    unittest.main()
