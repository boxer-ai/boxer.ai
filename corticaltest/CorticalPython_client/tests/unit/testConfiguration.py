"""
/*******************************************************************************
 * Copyright (c) cortical.io GmbH. All rights reserved.
 *  
 * This software is confidential and proprietary information.
 * You shall use it only in accordance with the terms of the
 * license agreement you entered into with cortical.io GmbH.
 ******************************************************************************/
"""
from cortical.client import ApiClient
API_KEY = "addYourKeyHere"
BASE_PATH="http://api.cortical.io/rest"
RETINA_NAME = "en_associative"
client = ApiClient(apiKey=API_KEY, apiServer=BASE_PATH)
