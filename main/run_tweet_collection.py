# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:41:31 2015
run preprocessing and onlineHDP scripts for tweet clustering
@author: srijith
"""

import sys, os, time

while True:
	os.system('python tweet_collect.py') 
	print('tweet collection over')
	os.system('python ModellingMultiClass.py')
	print('Classificaiton and posting over')                                                                                                                                
	

