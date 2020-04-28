#!/usr/bin/env python
# coding: utf-8

# In[1]:


conda install -c conda-forge lxml --yes


# In[2]:


import requests
import pandas as pd
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
r = requests.get(url)
df = pd.read_html(r.text)
df_toronto = df[0]


# In[3]:


#Drop rows with Borough = 'Not assigned'
df_toronto = df_toronto[df_toronto.Borough != 'Not assigned']


# In[8]:


#Replace '/' with ','
df_toronto['Neighborhood'] = df_toronto['Neighborhood'].str.replace('/', ',')
#Replace any empty cell with values from 'Borough'
df_toronto.Neighborhood.fillna(df_toronto.Borough, inplace=True)


# In[16]:


#Import geospatial data csv
geodata = pd.read_csv('https://cocl.us/Geospatial_data')
df_geo = pd.DataFrame(geodata)


# In[18]:


#Rename Column
df_geo.rename(columns = {'Postal Code':'Postal code'}, inplace = True)
df_geo
df_tor = df_toronto.merge(df_geo, on='Postal code', how = 'inner')
df_tor


# In[ ]:




