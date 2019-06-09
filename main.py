from html2text import unescape
import re
import ast
import pandas as pd
import numpy as np
import os.path
from textblob import TextBlob
import matplotlib
from matplotlib import pyplot as plt


def clean_csv():
    """ Read gameofthrones.csv into a dataframe, clean it & save as cleaned_got.csv """
    if os.path.exists('cleaned_got.csv') or not os.path.exists('gameofthrones.csv'):
        return

    df = pd.read_csv('gameofthrones.csv', header=0,
                     index_col='date', parse_dates=True)

    df.tweet = df.tweet.apply(lambda x: ast.literal_eval(x)  # handle strings that include bytestrings
                              .decode('utf-8').lower().strip())  # decode, lower case, remove trailing whitespace

    # remove line feed from the tweets
    df.tweet = df.tweet.replace(r'\n', ' ', regex=True)

    # replace duplicate whitespace
    df.tweet = df.tweet.replace(r'\s{2,}', ' ', regex=True)

    # decode html elements (like & < >)
    df.tweet = df.tweet.apply(unescape, unicode_snob=True)

    # date range between 2019-04-27 00:00:00 to 2019-05-04 00:00:00
    df = df.sort_index()
    df = df.loc[:'2019-05-04 00:00:00']

    df = df.dropna()  # dropping 3 null tweets

    df.to_csv('cleaned_got.csv')


def get_polarity(text):
    """ The polarity score is a float within the range [-1.0, 1.0]. """
    return TextBlob(text).sentiment.polarity


def get_subjectivity(text):
    """ Subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective. """
    return TextBlob(text).sentiment.subjectivity


def sentiment_analysis():
    """ Cleans the data and performs sentiment analysis on the tweets using TextBlob, saving this to got-sentiment.csv """
    clean_csv()

    print('Reading cleaned csv...')
    df = pd.read_csv('cleaned_got.csv', header=0,
                     index_col='date', parse_dates=True)
    print('DataFrame loaded.')

    if os.path.exists('got_sentiment.csv'):
        return

    print('Calculating tweet polarity & subjectivity...')
    df['polarity'] = df.tweet.apply(get_polarity)
    df['subjectivity'] = df.tweet.apply(get_subjectivity)
    df.to_csv('got_sentiment.csv')


def plot_sentiment():
    """ Plots polarity and subjectivity subplots from cleaned_got.csv """
    df = pd.read_csv('got_sentiment.csv', header=0,
                     index_col='date', parse_dates=True)
    print('Plotting polarity')
    df.polarity.plot(figsize=(64, 12), style='.')
    plt.savefig('polarity')


# plot_sentiment()
df = pd.read_csv('got_sentiment.csv', header=0,
                 index_col='date', parse_dates=True)

# remove tweets where we couldn't determine polarity
# zero_polarity = df[df.polarity == 0].index
# df = df.drop(zero_polarity)

df2 = df.drop(columns=['tweet', 'subjectivity'])

# take the average of the samples per 5 minutes
df2 = df2.resample('5T').mean()
print(df2.head())
print(df2.info())
df2.plot(figsize=(32, 6), style='-')
plt.savefig('polarity-2')
