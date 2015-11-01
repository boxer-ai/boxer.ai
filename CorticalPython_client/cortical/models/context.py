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

class Context(object):
    def __init__(self, fingerprint=None, context_label=None, context_id=None):
        #The semantic fingerprint representation of a context
        self.fingerprint = Fingerprint(**fingerprint) if isinstance(fingerprint, dict) else fingerprint # Fingerprint
        #The descriptive label of a context.
        self.context_label = context_label # str
        #The id of a context.
        self.context_id = context_id # int
        
