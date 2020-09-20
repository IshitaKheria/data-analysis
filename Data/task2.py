#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 23:13:07 2020

@author: ishitakheria
"""

'''
PROBLEM STATEMENT REFRAME
we want the properties of the population willing to fund the project with an amount greater than 20$ and belonging to
Sports or Environment Category

therefore constrains identified:- event_name = fund project, amount >= 20  and category = sports or environment.
'''

import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import table
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

'''
DATA CLEANING AND PRE-PROCESSING
- Applying constraints
- Removing extra features after applying constraints
- Handling missing or NaN values 
- Removing the duplicates based on category and session_id
- Finally checked the final features using heat map wrt category
'''
#extracting the data, applying the constrains and removing extra features

with open('data1.json')  as f:
    data= json.load(f)
df = pd.DataFrame.from_records(data['data'])
org = df.copy()
loc_org = pd.io.json.json_normalize(org.location)
#filtering the rows or applying the constraints 
df = df[((df.category == 'Sports') | (df.category == 'Environment')) & (df.event_name == 'Fund Project') & (df.amount >= 20)]
#converting location elements into different columns and storing the dataframe in loc variable
loc = pd.io.json.json_normalize(df.location)
#print(loc)
#dropping the location coloumn and the non-essential column 'client_time', 'amount' and 'event_name' in df 
df = df.drop(['location','client_time','amount','event_name'],axis=1)
#reseting the index for df
df = df.reset_index(drop = True)
#joing the 2 dataframes
df = pd.DataFrame.join(df,loc)
#print(df)
#sorted database 
df = df.sort_values(['category'])
#print(df)

#data cleaning for NaN values and duplicates

#replacing the nan values with 0.0 in the entire dataframe
df = df.replace(np.nan,0)
#dealing with duplicates using the unique session_id and category 
df = df.drop_duplicates(['session_id','category'])
#reseting the index
df = df.reset_index(drop = True)
#print(df)

dvf = df.copy()
#understanding the dataset feature relation by plotting a heat map which takes only non-categorical values

#gender is a categorical data so we convert it into numerical so that we can find a correlation
df['gender'] = df['gender'].replace({'M': 1,'F': 2,'U': 3})
#marital status is a categorical data so we convert it into numerical so that we can find a correlation
df['marital_status'] = df['marital_status'].replace({'single': 1,'married': 2})
#device is a categorical data so we convert it into numerical so that we can find a correlation
df['device'] = df['device'].replace({'android': 1,'iOS': 2})
#converting category to categorical data
df['category'] = df['category'].replace({'Sports': 1,'Environment': 2})
#replacing age intervals with it's mean
df['age'] = df['age'].replace({'18-24':22.5,'25-34':29.5,'35-44':39.5,'45-54':49.5,'55+':59.5})
#print(df.head())

#plotting the heat map
import seaborn as sb
plt.figure(figsize=(10,10))
corr = df.corr()
#print(corr)
heatMap = sb.heatmap(corr)
plt.show()
#from the heat map we can conclude that the category is nearly equally related to all the containg columns.


'''
DATA VISUALIZATION
- SCATTER MAP for understanding location 
- PIE CHART for rest using group by category -> age -> gender -> marital_status -> device
 '''

#cga = dvf.groupby(['category','gender','age','marital_status','device'])

cga=dvf.groupby(['category','gender','age','marital_status','device']).size().to_frame(name='count').reset_index()
#print(cga)

'''
c a g m d
size, color
'''
groupByLi = []
li = []
length = 1
for i in ['category','age','gender','marital_status','device']:
    groupByLi.append(i) 
    li1=[]
    length *= len(cga.groupby(i))
    
    for j in range(length):
        value = dvf.groupby(groupByLi).size()[j]
        li1.append(value)
        
    li.append(li1)
#print(li)
#-->[[3025, 3058], [1547, 366, 368, 375, 369], [714, 698, 135], [460, 254], [113, 347]]
    
colors = [['#294736', '#79b593'], ['#b9eef0', '#79d8db', '#3cc5c9', '#189fa3', '#29878a'], ['#ae56d6', '#8223ad', '#65357a'], ['#db429e', '#a30f68'], ['#dbac5a', '#8a5f13']]

plt.pie(li[4], colors=colors[4],radius=1.50, startangle=90)
plt.pie(li[3], colors=colors[3],radius=1.20, startangle=90)
plt.pie(li[2], colors=colors[2],radius=1.00, startangle=90)
plt.pie(li[1], colors=colors[1],radius=0.50, startangle=90)
plt.pie(li[0], colors=colors[0],radius=0.30, startangle=90)


centre_circle = plt.Circle((0,0),0.10,color='black', fc='white',linewidth=0)
fig.gca().add_artist(centre_circle)
fig = plt.gcf()

plt.axis('equal')
plt.tight_layout()
plt.show()


'''
GENERAL OBSERVATIONS
In the funding database
there are nearly equal number of people in:
    - both the categories 'Sports' and 'Environment'
    - male and female gender and abt 1/6th in unisex gender
    - 2/3rd people in each each category are married    
'''

'''
from the pie can conclude that in both the categories maximum contribuition is given by
- the age 18-24 (blue)
- married (pink)
- ios (beige n ochre)
- male or female (purple)
but this is common for all
'''


#scatter map for locations
pio.renderers.default = 'browser'

fig = px.scatter_mapbox(loc, lat="latitude", lon="longitude", hover_name="city", hover_data=["state", "zip_code"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


'''
state codes from the map:- (CLUSTERED AREAS)
NY, CA, IN, MA, CT, GA, OR, FL, NJ, MD, DE...
'''



































