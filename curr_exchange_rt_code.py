#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
from pandas import json_normalize
from pandas import to_datetime

######################### Extract Data from API Endpoint ####################################################

api_endpoint ='https://openexchangerates.org/api/latest.json?app_id=18e9471057894800a18b0192b52be7f8'

res=requests.get(api_endpoint)

if res.status_code==200:
    data=res.json()
else:
    print(f'error_message:{res.reason}')
    
##############################cleansing and transforming the data#############################################

df_latest_rate =json_normalize(data,sep='_')

df_latest_rate =df_latest_rate.drop(columns=['disclaimer','license'])

df_latest_rate = df_latest_rate.melt(id_vars=['timestamp','base'],var_name='transaction_curr',value_name='exchange_rt')

df_latest_rate[['var1','txn_curr']] =df_latest_rate['transaction_curr'].str.split('_',expand=True)

df_latest_rate =df_latest_rate.drop(columns='var1')

df_latest_rate.timestamp =to_datetime(df_latest_rate.timestamp, unit='s')

df_latest_rate['date']= df_latest_rate.timestamp.dt.date

df_latest_rate['time'] = df_latest_rate.timestamp.dt.time

df_latest_rate =df_latest_rate.drop(columns=['timestamp','transaction_curr'])


################################## loading the data to CSV file #################################################

df_latest_rate.to_csv(r'C:\Users\Muthu\Music\currency_exchange.csv',index=False)

print('file loaded successfully')



