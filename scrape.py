import secrets
import tweepy
import csv

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

with open('gameofthrones.csv', 'a') as file:
    writer = csv.writer(file)
    for tweet in tweepy.Cursor(
            api.search, tweet_mode='extended', q="#gameofthrones -filter:retweets", count=200, lang="en",
            since="2019-04-27").items():
        print(tweet.created_at, tweet.full_text)
        writer.writerow([tweet.created_at, tweet.full_text.encode('utf-8')])
    file.close()
