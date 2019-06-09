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
    if os.path.exists('cleaned_got.csv'):
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


clean_csv()

print('Reading cleaned csv...')
df = pd.read_csv('cleaned_got.csv', header=0,
                 index_col='date', parse_dates=True)
print('DataFrame loaded.')

print('Calculating tweet polarity & subjectivity...')
df['polarity'] = df.tweet.apply(get_polarity)
df['subjectivity'] = df.tweet.apply(get_subjectivity)

print('Plotting polarity')
df.polarity.plot()
plt.savefig('polarity')
