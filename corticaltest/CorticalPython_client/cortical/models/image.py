#!/usr/bin/env python
"""
/*******************************************************************************
 * Copyright (c) cortical.io GmbH. All rights reserved.
 *  
 * This software is confidential and proprietary information.
 * You shall use it only in accordance with the terms of the
 * license agreement you entered into with cortical.io GmbH.
 ******************************************************************************/
"""
from cortical.models.fingerprint import Fingerprint

class Image(object):
    def __init__(self, fingerprint=None, image_data=None):
        #The semantic fingerprint representation.
        self.fingerprint = Fingerprint(**fingerprint) if isinstance(fingerprint, dict) else fingerprint # Fingerprint
        #Image data in base64 encoding.
        self.image_data = image_data # list[byte]
        
