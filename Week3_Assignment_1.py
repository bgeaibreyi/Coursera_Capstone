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
df_toronto.shape

# In[ ]:




