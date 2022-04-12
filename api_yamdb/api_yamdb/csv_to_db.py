import pandas
import sqlite3
import os


csvcat = '../static/data/'

for file in os.listdir(csvcat):
    filename = os.path.splitext(file)[0]
    df = pandas.read_csv(csvcat + file)
    conn = sqlite3.connect('db.sqlite3 3')
    df.to_sql(filename, conn, if_exists='append', index=False)
