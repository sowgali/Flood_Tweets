#import tweet_collect
#import ModellingMultiClass
#import retweet_maker
import sys, os, time

while True:
	#tweet_collect.tweet_collection()
	# os.system('nohup python tweet_collect.py &') 
	os.system('python tweet_collect.py') 
	print("Tweet collection done")
	#need_list_id, supply_list_id = ModellingMultiClass.classify()
	# os.system('nohup python ModellingMultiClass.py &')
	os.system('python ModellingMultiClass.py')
	print("Classified and posted in Twitter")



















	
	#retweet_maker.retweet(supply_list_id)
	#retweet_maker.retweet(need_list_id)
	#print("Posted in Twitter")
