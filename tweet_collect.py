import tweepy
from tweepy import Stream,StreamListener
import json
import csv
import sys
import pandas as pd
import os
import time
import re

def contains_phone(text):
    phonePattern=re.compile(r'''
                # don't match beginning of string,number can start anywhere
    (\d{3})     # area code is 3 digits (e.g. '800')
    \D*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    \D*         # optional separator
    (\d{4})     # rest of number is 4 digits (e.g. '1212')
    \D*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
    $           # end of string
    ''',re.VERBOSE)
    # return len(phonePattern.findall(text))
    if len(phonePattern.findall(text)) > 0:
        return True
    else :
        return False

def tweet_collection():
	consumer_key='x5xOBEj6Lf4ZvMxvLEt8ZGu9a'
	consumer_secret='mmVr6m8c39YgE3BvuL4eyOe1bwVUWRWYyqOq1TrNwULdh3ojSZ'
	access_token = '1031468370774831104-Rs0lPxwHmjEwXuge0Efea6PvMnuSRX'
	access_token_secret = 'RZGbpmZe4h5OLAF14P3WrtHHkqV5PMliKEIhmLBwIJI6N'
	email_reg = '\S+@\S+\.\S+'
	contact_reg = '\d{10}'
    #creation of auth variable which will give us access to API
	auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    #getting the access
	auth.set_access_token(access_token,access_token_secret)
    #i=0
	outfile=open('collection.csv', "w")

	csv1 = csv.writer(outfile)
	csv1.writerow(['Id','Created_at','Text'])

	class listener(StreamListener):
		i=0
		print("tweet collect file")
		print(i)
		def on_data(self,data):

						
			if(self.i==1):
				outfile.close()
				print(self.i)
				print("ended")
				sys.exit()

				
			#json.dump(data,outfile)
			#outfile.write()
			#print(self.i)
			tweet = json.loads(data)
			try:

				#print(tweet.keys())
				if('extended_tweet' in tweet.keys()):
					text=tweet['extended_tweet']['full_text'].encode('utf-8')
				else:
					text=tweet['text'].encode('utf-8')
				#print("data:{}".format(self.i))
				#print(tweet['created_at'],text)	
				row = (tweet['id'],tweet['created_at'],text)
				print(text)
				text = str(text)
				if ((('Karnataka' in text) or ('karnataka' in text) or ('KARNATAKA' in text) or ('#KarnatakaFloods' in text) or ('#KarnatakaFloods2019' in text) or ('#Karnataka' in text)) and( ('food' in text) or ('kit' in text) or ('volunteer' in text) or ('suppl' in text) or ('medic' in text) or ('requir' in text) or ('water' in text) or ('avail' in text) or ('need' in text) or ('call' in text) or ('resource' in text) or ('contact' in text) or ('rescue' in text))):
					print("First if crossed")
					if 'sex' in text or 'porn' in text or 'callgirl' in text or 'partying' in text or 'crore' in text or 'rupee' in text or 'Eid' in text or 'lakh' in text or 'tour' in text or 'vacation' in text or 'dance' in text or 'death' in text or 'Death' in text or 'die' in text or 'died' in text or 'ManVsWild' in text or '#ManVsWild' in text or 'Death Toll' in text or 'losses' in text or 'visit' in text or 'visited' in text or 'Visited' in text or 'report' in text or 'bribe' in text or 'black money' in text or b'survey' in text or 'partying' in text or 'beef' in text or 'deadliest' in text:
						print("Filtered words found")
						return
					#match = re.search(contact_reg, text)
					#email_match = re.search(email_reg, text)
                        		#if  contains_phone(text) or email_match:
					#if match.group():
						#print('Contact found: {0}'.format(match.group()))		
					values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
					print("values " + str(values))
					csv1.writerow(values)
					self.i+=1
					print('tweet added:{}'.format(self.i))
				else:
					print('Contact not found in a tweet satisfying previous criteria')
#				else:
#					print("not added")
			except:
				time.sleep(1)

			


		def on_error(self,status):
			print(status)


	tweets=Stream(auth,listener(),tweet_mode="extended")



	tweets.filter(track=["standwithkarnataka","karnataka flood","karnatakafloods","north karnataka floods"
		"#karnatakaflood","#karnatakahealth","karnataka health","#prayforkarnataka "
		"#Rescuekarnataka","karnatakarelieffund","karnataka relief","rebuild karnataka","#doforkarnataka ",
		#"#anbodukochi ",
		"#HelpKarnatka","#karnatakahelp","#KarnatakaDonationChallenge ",
		"#IndiaWithKarnataka","#KarnatakaSOS", "#CMRF", "#KarnatakaFloods", "#NorthKarnatakaFloods", "#BelagaviRains","#SaveUttaraKarnataka", "karnataka_rescue",#"anbodukochi",
		 "karnataka rescue","#resources karnataka", "resources karnataka","#OneNationYouth", "#prayforuttarkarnataka"])
#	tweets.filter(track=["kerala flood","keralafloods","#keralaflood","#Rescuekerala","#KeralaSOS","kerala_rescue", '#KeralaFloodRelief', '#SOSKerala'])
	tweets.filter(languages=["en"])
	



#while True:	
tweet_collection()

#print('starting code...') 
#tweet_collection()
#print("printing CSV MAKER...")

