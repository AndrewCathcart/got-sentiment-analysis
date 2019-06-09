from html2text import unescape
import re
import ast
import pandas as pd
import numpy as np
import os.path


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
    df = df.loc[:'2019-05-04 00:00:00']

    df.to_csv('cleaned_got.csv')


clean_csv()

print('Reading cleaned csv...')
df = pd.read_csv('cleaned_got.csv', header=0,
                 index_col='date', parse_dates=True)
print('DataFrame loaded.')
