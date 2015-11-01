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
import requests


class ApiClient:

    def __init__(self, apiKey=None, apiServer=None):
        if apiKey == None:
            raise Exception('You must pass an apiKey when instantiating the APIClient')
        self.apiKey = apiKey
        self.apiServer = apiServer
        self.cookie = None
    

    def _callAPI(self, resourcePath, method, queryParams, postData, headers={}):

        url = self.apiServer + resourcePath
        headers['api-key'] = self.apiKey
        response = None
        
        if method == 'GET':
            response = requests.get(url, params=queryParams, headers=headers)

        elif method == 'POST':
            response = requests.post(url, params=queryParams, headers=headers, data=postData)

        else:
            raise Exception('Method ' + method + ' is not recognized.')

        if response.status_code != 200:
            raise Exception("Response " + str(response.status_code) + ": " + response.content)
        return response
        
