import csv
import pandas as pd
import ast

df = pd.read_csv('gameofthrones.csv', delimiter=',', header=0, dtype={"date": str, "tweet": bytes})
# cleaning
df['tweet'] = df['tweet'].apply(lambda x: ast.literal_eval(x).decode('utf-8'))
df['tweet'] = df['tweet'].apply(lambda x: x.lower())
df = df.replace(r'\n', ' ', regex=True)
print(df['tweet'])
