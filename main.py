from html2text import unescape
import re
import ast
import pandas as pd
import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import seaborn as sns


def import_clean_save():
    """ Read gameofthrones.csv into a dataframe, clean it & save to a pickled file cleaned.pkl """
    df = pd.read_csv('gameofthrones.csv', delimiter=',', header=0)

    df.date = df.date.apply(lambda x: pd.to_datetime(x))
    df.tweet = df.tweet.apply(lambda x: ast.literal_eval(x)  # handle strings that include bytestrings
                              .decode('utf-8').lower().strip())  # decode, lower case, remove trailing whitespace
    # remove line feed from the tweets
    df.tweet = df.tweet.replace(r'\n', ' ', regex=True)
    # replace duplicate whitespace
    df.tweet = df.tweet.replace(r'\s{2,}', ' ', regex=True)
    # decode html elements (like & < >)
    df.tweet = df.tweet.apply(unescape, unicode_snob=True)
    # date range between 2019-04-27 00:00:00 to 2019-05-04 00:00:00
    df = df[(df['date'] <= '2019-05-04 00:00:00')]
    df.to_pickle('cleaned.pkl')


# import_clean_save()
print('loading pickled DataFrame...')
df = pd.read_pickle('cleaned.pkl')
print('DataFrame loaded.')

df_by_day = df.groupby([df.date.dt.month, df.date.dt.day])

df_count_by_day = df_by_day.count()
df_count_by_day.index.names = ['month', 'day']
df_count_by_day = df_count_by_day.drop('date', axis=1)
df_count_by_day.sort_index(inplace=True)
df_count_by_day = df_count_by_day.reset_index()
# print(type(df_count_by_day))
# np_array = df_count_by_day.as_matrix()
# print(np_array)
sns.pairplot(df_count_by_day)
plt.savefig('tmp.png')
