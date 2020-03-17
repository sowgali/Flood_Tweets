#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 14:42:01 2018

@author: uddipta
"""
import tweepy
from tweepy import *
import os
 
# Consumer keys and access tokens, used for OAuth
def retweet(statuses):
	ck='x5xOBEj6Lf4ZvMxvLEt8ZGu9a'# (API key)

	cks='mmVr6m8c39YgE3BvuL4eyOe1bwVUWRWYyqOq1TrNwULdh3ojSZ' 
	access_token = '1031468370774831104-Rs0lPxwHmjEwXuge0Efea6PvMnuSRX'
	access_token_secret = 'RZGbpmZe4h5OLAF14P3WrtHHkqV5PMliKEIhmLBwIJI6N'
	 
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(ck, cks)
	auth.set_access_token(access_token, access_token_secret)
	 
	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)

	# Creates the user object. The me() method returns the user whose authentication keys were used.
	user = api.me()



	# Construct the API instance
	api = tweepy.API(auth)

	# Creates the user object. The me() method returns the user whose authentication keys were used.
	user = api.me()
	 
	#print('Name: ' + user.name)
	
	 
	# Sample method, used to update a status
	# api.update_status('Hello Form RBI Lab!')


	

	#read text from csv

	
	print("In retweet maker file")
	for ids in statuses:

		print(ids)
		i=1   #0 for urgent, 1 for SUPPLY_REQ and so on
		try:
			api.retweet(ids)
		except:
			continue
