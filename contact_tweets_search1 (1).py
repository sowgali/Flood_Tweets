import tweepy
from tweepy import Stream, StreamListener
import json
import csv
import sys
import pandas as pd
import os
import time
import re
from tweepy import *
import os
import datetime

TWEETS = pd.DataFrame(columns = ['Id', 'CreatedAt', 'Text'])


def contains_phone(text):
    phonePattern = re.compile(r'''
                # don't match beginning of string,number can start anywhere
    (\d{3})     # area code is 3 digits (e.g. '800')
    \D*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    \D*         # optional separator
    (\d{4})     # rest of number is 4 digits (e.g. '1212')
    \D*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
    $           # end of string
    ''', re.VERBOSE)
    # return len(phonePattern.findall(text))
    if len(phonePattern.findall(text)) > 0:
        return True
    else:
        return False


def get_keyword_tweets(keyword, per_page = 100, max_count=50000):
    # rohan's Political tweet collection app keys
    consumer_key = 'JBbZgOVsUDUbIyI3LLpS39b5A'
    consumer_secret = '6jZ4JViRsK302RTsc6KDfBccMS4mI4fGjHzScxOCJA7PvWFvIo'
    access_token = '568966944-T4wQcwC2Lm8fh2Vcgq02vY371RRlqDYqVOxx5sgE'
    access_secret = '6K7PqTYXWNx0OJoHpNuFwbEOfuXiUoZEkAUCGsSzRyvhs'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    print('Fetching tweets for keyword: {0}'.format(keyword))
    tweets = api.search(q = keyword, lang = "en", count = per_page,  result_type='recent', tweet_mode='extended')
    tweets_length = len(tweets)
    print('Tweets fetched: {0}'.format(tweets_length))
    max_id = int(tweets[tweets_length-1].id) - 1

    count = 0
    while True:
            try:
                    new_tweets = api.search(q = keyword, lang = "en", count = per_page, max_id = max_id, result_type='recent', tweet_mode='extended')
                    if len(new_tweets) == 0:
                        print('No new tweets')
                        break
                    if len(tweets) >= max_count:
                        print('Max count for tweets reached: {0}'.format(len(tweets)))
                        break
                    analyze_tweets(new_tweets)
                    tweets.extend(new_tweets)
                    print('Tweets fetched in iteration {0}: {1}'.format(count, len(new_tweets)))
#                 print('Total tweets: {0}'.format(len(tweets)))
                    max_id = new_tweets[-1].id -1
                    count +=1
            except Exception as e:
                    print('Exception {0} while fetching tweets for {1}'.format(e, keyword))
                    break
            print('Returning {0} tweets'.format(len(tweets)))
            return tweets

def analyze_tweets(tweets):
    outfile=open('contact_tweets_filtered.csv', "a")
    fullfile = open('unfiltered_tweets_rohan.csv', "a")
    csv2 = csv.writer(fullfile)
    csv2.writerow(['Id','Created_at','Text'])
    csv1 = csv.writer(outfile)
    csv1.writerow(['Id','Created_at','Text'])
    contact_reg = '\d{10}'
    email_reg = '\S+@\S+\.\S+'
    for tweet in tweets:
                text = tweet.full_text.encode('utf-8')
                if 'RT @' in text:
                    continue
                tweet_id = tweet.id_str
                created_at = tweet.created_at
                csv2.writerow([tweet_id, text, str(created_at)])
                if True or (('food' in text) or ('suppl' in text) or ('medic' in text) or ('requir' in text) or ('water' in text) or ('avail' in text) or ('need' in text) or ('call' in text) or ('resource' in text) or ('contact' in text)):
                    if 'sex' in text.lower() or 'porn' in text.lower() or 'callgirl' in text.lower() or 'crore' in text.lower() or 'rupees' in text.lower() or 'million' in text.lower() or 'onam' in text.lower() or 'vacation' in text.lower() or 'travel' in text.lower() or 'tour' in text.lower():
                        continue
                                        # Check if the tweet has a contact number
                    match = re.search(contact_reg, text)
                email_match = re.search(email_reg, text)
                        #if contains_phone(text) or email_match:
                if match or email_match:
                    if created_at.day != datetime.datetime.today().day:
                        print('Skipping old tweet from: {0}'.format(created_at))
                        continue
                # if match.group() == '201' and 'maharashtrafloods2018' in text.lower()  and not email_match:
                #    print('Removing tweet with 2018 in text')
                #    continue
                    csv1.writerow([tweet_id, text, str(created_at)])
                                    #            self.i+=1
                    print('Accepted tweet with timestamp: {0}'.format(created_at))
                                #retweet([tweet_id])
                maintain_sorted_tweets(tweet_id, created_at, text)
                #if match:
                                   #    print('tweet containing contact number: {0}'.format(match.group()))
                if email_match:
                    print('tweet containing email id: {0}'.format(email_match.group()))
                print(text)

def maintain_sorted_tweets(tweet_id, tweet_created_at, tweet_text):
    global TWEETS
    TWEETS = TWEETS.append({'Id': tweet_id, 'CreatedAt': tweet_created_at, 'Text': tweet_text}, ignore_index=True)
    TWEETS.sort_values(by = ['CreatedAt'], ascending=True, inplace=True)

def post_tweets():
    global TWEETS
    print('Posting all tweets in sorted by time')
    for count, row in TWEETS.iterrows():
        print('Posting tweet with timestamp: {0}'.format(row['CreatedAt']))
        retweet([row['Id']])
    print('All tweets posted, truncating the dataframe')
    TWEETS = pd.DataFrame(columns = ['Id', 'CreatedAt', 'Text'])
    print(TWEETS.head())

def collect_tweets():
    #keywords = {'maharashtra email':2000}
    keywords = {'KarnatakaSOS':1000, 'karnatakafloodreliefs':1000, 'karnatakafloodrelief':1000, 'karnataka floods contact':1000, 'karnataka email':1000, '#karnatakafloods resources':1000, 'karnatakarelief':1000, 'karnatakafloods':1000}
    for word, max_count in keywords.items():
            tweets = []
            try:
            #new_tweets = api.search(q = word, lang = "en", count = 100,  result_type='recent', tweet_mode='extended')
                new_tweets = get_keyword_tweets(word, max_count=max_count)
                print('Total tweets for keyword: {0}: {1}'.format(word, len(new_tweets)))
                tweets.extend(new_tweets)
            except Exception as e:
                print('Exception {0} while fetching tweets for {1}'.format(e, word))
    post_tweets()

def retweet(statuses):
        # All keys from Srijith sir's twitter account
        ck='pRYfMwXre3aYDjcGc58ImukOe'  # (API key)

        cks='UDmIZCxSVfHTeDWLz60NTTFrAnXgpVkBjDUcThv87nZm4MsMNt'
        access_token = '40830950-h2oiJqcKOUhEMxgcju7faInQX7GijGg88VIum1Y0a'
        access_token_secret = 'wYsiobtqobLMZ7un0TnFvp6Ql8T4MXrggXhan7DOs4cPx'

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
        for ids in statuses:
            i=1   #0 for urgent, 1 for SUPPLY_REQ and so on


            try:
                # Send the tweet.
                api.retweet(ids)
            except Exception as e:
                print('Exception while retweeting: {0}'.format(e))
                continue


def main():
    import time
    while True:
        collect_tweets()
        time.sleep(900)

if __name__ == "__main__":
        main()
