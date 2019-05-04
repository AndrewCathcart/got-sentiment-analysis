import secrets

import tweepy
import csv

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

with open('gameofthrones.csv', 'a') as file:
    writer = csv.writer(file)
    for tweet in tweepy.Cursor(api.search, q="#gameofthrones", count=200, lang="en", since="2019-04-27").items():
        print (tweet.created_at, tweet.text)
        writer.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    writer.close()