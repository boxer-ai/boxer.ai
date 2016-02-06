# -*- coding: utf-8 -*-
"""
Created on Tue May 05 21:40:54 2015

@author: Matt
"""

# Using ftputil (not part of standard library)
# see http://ftputil.sschwarzer.net/trac

import ftputil

# Download some files from the login directory.
host =  ftputil.FTPHost('ftp.sec.gov', 'anonymous', 'mattsekerke@gmail.com')
names = host.listdir(host.curdir)

# Pass unicode string from list of names in order to download
# host.download(names[2],'SEC_README.TXT')

host.chdir('edgar')
names = host.listdir(host.curdir)
# host.download(names[5],'SEC_README.TXT')

host.chdir('full-index')
host.listdir(host.curdir)

# Get JSON index of directory contents
import json

host.download(u'index.json','sec_index.json')
index = open('sec_index.json')  
idx = json.load(index)
directory = idx['directory']
item = directory['item']

# Get index of company identifiers if updated
host.download_if_newer(u'master.idx','master_index.idx')

import pandas as pd

index_reader = pd.read_table('master_index.idx', sep="|", skiprows = 8)

test = index_reader[index_reader['CIK'] == '1000209'] # Particular company
test = index_reader[index_reader['Date Filed'] == '2015-09-08'] # Particular date

# Iterate over selection and save files (actually XBRL files)
url_list = test['Filename']
i = 1
for url in url_list[0:3]:
    save_name = 'test_file' + str(i) + '.txt'
    host.download(url, save_name)
    i += 1
    
