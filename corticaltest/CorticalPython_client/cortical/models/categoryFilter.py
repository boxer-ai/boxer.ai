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

class CategoryFilter(object):

    def __init__(self, categoryName=None, positions=None):
        #The descriptive label for a CategoryFilter name
        self.categoryName = categoryName # str
        #The positions of a Fingerprint
        self.positions = positions # list[int]
        
