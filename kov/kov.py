import sys
import tweepy
import key as tw
import pprint
import re
import datetime
import time
import random

SINCE_ID = 0
reloadtime_for_lib = 0

def init():
    consumer_key = tw.tokens['consumer_key']
    consumer_secret = tw.tokens['consumer_secret_key']
    access_token_key = tw.tokens['access_token_key']
    access_token_secret_key = tw.tokens['access_token_secret_key']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret_key)
    api = tweepy.API(auth)

    return api

def get_kohuitweets(api):
    kovroid_texts = []
    kovroid_tweets = api.user_timeline('kovroid')

    for tweet in kovroid_tweets:
        kovroid_texts += [tweet.text]

    return kovroid_texts

def clean_text(kovroid_texts):
    cleaned_texts = list(map(lambda x:re.sub('@.*\s','',x),kovroid_texts))
    return cleaned_texts

def get_newmention(api):
    global SINCE_ID
    mention_tweets = api.mentions_timeline(since_id = SINCE_ID)
    
    if mention_tweets == []:
        return mention_tweets

    SINCE_ID = mention_tweets.since_id
    return mention_tweets

def check_kovri(mention_tweets,kovroid_texts):
    kovri_tweets = []
    for mention_tweet in mention_tweets:
        mention_texts = clean_text([mention_tweet.text])
        text = mention_texts[0]
        for kovroid_text in kovroid_texts:
            if text in kovroid_text or kovroid_text in text:
                kovri_tweets = [mention_tweet]
                break

    return list(reversed(kovri_tweets))
    
def kovru(api,kovri_tweets,kovroid_texts):
    for tweet in kovri_tweets:
        reply_text = kovroid_texts[random.randint(0,len(kovroid_texts)) - 1]
        api.update_status("@" + tweet.user.screen_name + " " + reply_text, tweet.id)
    
def reload_kovroid_lib(api):
    kovroid_texts = get_kohuitweets(api)
    kovroid_texts = clean_text(kovroid_texts)
    reloadtime_for_lib = time.time() + 900

    return kovroid_texts
    

def main():
    random.seed()
    api = init()
    
    global SINCE_ID
    mention_tweets = api.mentions_timeline()
    SINCE_ID = mention_tweets.since_id

    kovroid_texts = reload_kovroid_lib(api)

    while True:
        time.sleep(60)

        mention_tweets = get_newmention(api)
        kovri_tweets = check_kovri(mention_tweets,kovroid_texts)

        kovru(api,kovri_tweets,kovroid_texts)
        
        if reloadtime_for_lib <= time.time():
            kovroid_texts = reload_kovroid_lib(api)

if __name__ == '__main__':
    main()
