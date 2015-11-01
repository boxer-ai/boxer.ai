#!/usr/bin/env python
"""
/*******************************************************************************
 * Copyright (c) cortical.io GmbH. All rights reserved.
 *  
 * This software is confidential and proprietary information.
 * You shall use it only in accordance with the terms of the
 * license agreement you entered into with cortical.io GmbH.
 ******************************************************************************/

Add all of the modules in the current directory to __all__
"""
import os

__all__ = []

for module in os.listdir(os.path.dirname(__file__)):
    if module != '__init__.py' and module[-3:] == '.py':
        __all__.append(module[:-3])

