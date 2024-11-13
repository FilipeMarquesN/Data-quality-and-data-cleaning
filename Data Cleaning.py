# -*- coding: utf-8 -*-
"""

@author: Filipe Marques, Leonor Fandinga, Marcos Torres
Realizado no Ambito da cadeira de Fundamentos da ciencia de dados
Dados obtidos em:https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata/data
"""

import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('Airbnb_Open_Data.csv')


#DROPS

#Drop Collumn Missing Values because of not using in this work
df.drop(['house_rules','license'], axis='columns', inplace=True)

#Drop Collumn constants
df.drop(['country code','country'], axis='columns', inplace=True)

#Drop Because of a lot of missing values and not use of this to our ansewer we removed this collumns
df = df.drop(columns=['last review'])
df = df.drop(columns=['number of reviews'])
df = df.drop(columns=['reviews per month'])

#Remove missing in Groups
df = df.dropna(subset=['neighbourhood', 'neighbourhood group', 'lat', 'long', 'price','availability 365','instant_bookable','cancellation_policy'])

#Convert Values to floats because of values in String

#Convert Price e fee to Float
df['price'] = df['price'].str.replace('$', '')
df['price'] = df['price'].str.replace(',', '.')
df['price'] = df['price'].astype('float')

df['service fee'] = df['service fee'].str.replace('$', '')
df['service fee'] = df['service fee'].str.replace(',', '.')
df['service fee'] = df['service fee'].astype('float')

#Set missing 

#Set missing to 0
df['minimum nights'] = df['minimum nights'].fillna(0)
df['service fee'] = df['service fee'].fillna(0)

#Set missing to False
df['host_identity_verified'] = df['host_identity_verified'].fillna('False')

#Set Max and Min

df['availability 365'] = df['availability 365'].clip(upper=365)
df['availability 365'] = df['availability 365'].clip(lower=0)

df['minimum nights'] = df['minimum nights'].clip(lower=0)

df['minimum nights'] = df['minimum nights'].clip(upper=60)

df['Construction year'] = df['Construction year'].fillna(2003)

#Change names to correct names

#Set groups to correct names
df.loc[df['neighbourhood group'] == 'manhatan', 'neighbourhood group'] = 'Manhattan'
df.loc[df['neighbourhood group'] == 'brookln', 'neighbourhood group'] = 'Brooklyn'

#Make the pdf with report

profile = ProfileReport(df, title="Profiling Report")
profile.to_file("report.html")