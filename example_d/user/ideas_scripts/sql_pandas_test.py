import sqlite3
import pandas as pd
import sys
from sql import create_db_conn

###
print("diff row and following")
#query = "select timestamp/1000 from tracker_pnl order by timestamp desc"
query = "select trigger_price_to_put_in_position tt from radar_list where trigger_price_to_put_in_position >= 0.48 and trigger_price_to_put_in_position <=0.49 order by trigger_price_to_put_in_position desc"
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.diff.html
df = pd.read_sql(query, con = create_db_conn())
print(df)
print(df.diff(periods=-1)) # hace la diferencia entre row y following row 
df_diff = df.diff(periods=-1)
print("....")
print(df_diff)
print("....")
df_diff['original_value'] = df
print(df_diff)
print("....")
df_diff['cuanto'] = 100*df_diff['tt']/df_diff['original_value']
print(df_diff)
print("++++++++++++++++++ todo junto en un mismo df")
df = pd.read_sql(query, con = create_db_conn())
df['diff'] = df.diff(periods=-1)
df['distance%'] = 100*df['diff']/df['tt']
print(df)
#sys.exit(66)
print("-----------------")

query = "select trigger_price_to_put_in_position, count(*) count from pnl_hist where order_status='PNL' group by trigger_price_to_put_in_position order by 2 desc limit 5;"
df = pd.read_sql(query, con = create_db_conn())
print(df)
dft = df.set_index('count').transpose()
print(dft)

sys.exit(66)
###
print("diff row and previous")
query = "select timestamp/1000 tt from tracker_pnl order by timestamp asc"
df = pd.read_sql(query, con = create_db_conn())
print(df)
print(df.diff()) # hace la diferencia entre row y previous row
####
print("df is type: " + str(type(df)))
for index, row in df.iterrows():
    #print(row['tt'])
    nada=1

print("-----------------")
df2 = df.diff()
count1 = 0
for index, row in df2.iterrows():
    #print(row['tt'])
    if row['tt'] == 1:
        count1 += 1
    nada = 1 
print("count1: " + str(count1))

print("-----------------")
print("df mean: " + str(df2.mean(axis=0))) # mean is average
print("-----------------")
print("df mode: " + str(df2.mode(axis=0))) # mode return the highest frequency value in a series
print("-----------------")
print("df value_counts(): " + str(df2.value_counts().head(20))) # frequency
print("-----------------")
print("df last 20 pnl duration: " + str(df2.tail(20)))
last20pnl_list = []
for index, row in df2.tail(20).iterrows():
    print("row: " + str(row['tt']))
    last20pnl_list.append(row['tt'])
print("last20pnl_list.append(row['tt']): " + str(last20pnl_list))
print("-----------------")
import numpy as np
#create example data
col1 = np.random.randint(0,10,size=10)
df = pd.DataFrame()
print("++++")
print("raw df")
print(df)
print("++++")
print("df + col1")
df["col1"] = col1
print(df)
print("++++")
print("df + col1 + result")
df["result"] = [0]*len(df)
print(df)
#slow computation
for i in range(len(df)):
    if i == 0:
        df["result"][i] = np.nan
    else:
        df["result"][i] = np.log(df["col1"][i]/df["col1"][i-1])
'''
query = "select * from tracker_pnl"
damian@DESKTOP-2UIJB1T:~/.local/lib/python3.8/site-packages/binance_d/example_d/user$ python3 ./sql_pandas_test.py
         order_id      timestamp        rp
0      6500259306  1653945451148  0.821755
1      6500408353  1653945445529  0.641639
2      6500428296  1653944402294  0.423154
3      6500522244  1653944401025  0.743991
4      6500541198  1653944400645  0.332445
...           ...            ...       ...
10934  6864863392  1655746792905  0.749761
10935  6864880419  1655746782361  0.713168
10936  6864897579  1655747123392  0.806650
10937  6864901922  1655747029815  0.755233
10938  6864905092  1655747024387  0.741113

[10939 rows x 3 columns]

'''


'''
query = "select timestamp/1000 from tracker_pnl order by timestamp asc"
       timestamp/1000
0                 NaN
1               237.0
2               725.0
3              3952.0
4              2527.0
...               ...
10934             5.0
10935            94.0
10936            21.0
10937             2.0
10938             5.0

[10939 rows x 1 columns]
'''

