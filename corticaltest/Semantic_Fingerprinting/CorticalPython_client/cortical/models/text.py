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

class Text(object):
    def __init__(self, text=None, fingerprint=None):
        #The text as a string
        self.text = text # str
        #The semantic fingerprint representation of the text.
        self.fingerprint = Fingerprint(**fingerprint) if isinstance(fingerprint, dict) else fingerprint # Fingerprint
        
