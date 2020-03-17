import tweepy
from tweepy import Stream,StreamListener
import json
import csv
import sys
import pandas as pd
import os
import time
import re

def tweet_collection():
	consumer_key='x5xOBEj6Lf4ZvMxvLEt8ZGu9a'
	consumer_secret='mmVr6m8c39YgE3BvuL4eyOe1bwVUWRWYyqOq1TrNwULdh3ojSZ'
	access_token = '1031468370774831104-Rs0lPxwHmjEwXuge0Efea6PvMnuSRX'
	access_token_secret = 'RZGbpmZe4h5OLAF14P3WrtHHkqV5PMliKEIhmLBwIJI6N'
	contact_reg = '\d{10}'
    #creation of auth variable which will give us access to API
	auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    #getting the access
	auth.set_access_token(access_token,access_token_secret)
    #i=0
	outfile=open('contact_tweets.csv', "w")

	csv1 = csv.writer(outfile)
	csv1.writerow(['Id','Created_at','Text'])

	class listener(StreamListener):
		i=0
		def on_data(self,data):

						
			#if(self.i==10):
			#	outfile.close()
			#	print(self.i)
			#	print("ended")
			#	sys.exit()

				
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

				if (('food' in text) or ('suppl' in text) or ('medic' in text) or ('requir' in text) or ('water' in text) or ('avail' in text) or ('need' in text) or ('call' in text) or ('resource' in text) or ('contact' in text)):
					# Check if the tweet has a contact number
					match = re.search(contact_reg, text)
					if match:
						print('Contact found: {0}'.format(match.group()))		
						values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
						#csv1.writerow(values)
						self.i+=1
						tweet_id = row[0]
						print('Accepted tweet: {0}'.format(text))
						#retweet([tweet_id])
						print('tweet posted with contact number: {0}'.format(match.group()))
						#print('tweet added:{}'.format(self.i))
					else:
						print('Contact not found in a tweet satisfying previous criteria')
						print(text)
#				else:
#					print("not added")
			except:
				time.sleep(1)

			


		def on_error(self,status):
			print(status)


	tweets=Stream(auth,listener(),tweet_mode="extended")



#	tweets.filter(track=["kerala","standwithkerala","kerala flood","keralafloods","its_trivandrum",
#		"keralam","#anbodutrivandrum","#keralaflood","#prayforkerala "
#		"#Rescuekerala","keralarelieffund","#godsowncountry","#doforkerala ",
#		"#anbodukochi ","#HelpKerala ","#KeralaDonationChallenge ",
#		"#IndiaWithKerala","#KeralaSOS","kerala_rescue","anbodukochi","kochi","cochin","ernakulam","aluva","chengannur","alappey",#"Alappuzha","Alwaye"])
#	tweets.filter(track=['keralafloods', '#anbodukochi', '#Rescuekerala', 'kerala_rescue', "kochi","cochin","ernakulam","aluva","chengannur",'alappey', "Alappuzha","Alwaye" ])
	tweets.filter(track=['karnatakafloods resource'])
	tweets.filter(languages=["en"])
	
import tweepy
from tweepy import *
import os

# Consumer keys and access tokens, used for OAuth
def retweet(statuses):
	# All keys from Srijith sir's twitter account	
        ck='pRYfMwXre3aYDjcGc58ImukOe'# (API key)

        cks='UDmIZCxSVfHTeDWLz60NTTFrAnXgpVkBjDUcThv87nZm4MsMNt'
        access_token = '40830950-K24hYJVU9A7L5KqpKa2RYqgX5DMAynET0U8Uylzy4'
        access_token_secret = '6orxT4ut33ocodbqOys8hab7noiTp2REVbma5K8IaQckr'

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



        for ids in statuses:


            i=1   #0 for urgent, 1 for SUPPLY_REQ and so on


            try:
                # Send the tweet.
                api.retweet(ids)
            except:
                continue



#while True:	
tweet_collection()

#print('starting code...') 
#tweet_collection()
#print("printing CSV MAKER...")

