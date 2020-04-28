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


# Drop rows with Borough = 'Not assigned'
df_toronto = df_toronto[df_toronto.Borough != 'Not assigned']


# In[8]:


# Replace '/' with ','
df_toronto['Neighborhood'] = df_toronto['Neighborhood'].str.replace('/', ',')
# Replace any empty cell with values from 'Borough'
df_toronto.Neighborhood.fillna(df_toronto.Borough, inplace=True)


# In[20]:


# Import geospatial data csv
geodata = pd.read_csv('https://cocl.us/Geospatial_data')
df_geo = pd.DataFrame(geodata)


# In[36]:


# Rename Column
df_geo.rename(columns = {'Postal Code':'Postal code'}, inplace = True)
df_geo
df_tor = df_toronto.merge(df_geo, on='Postal code', how = 'inner')
df_tor


# In[37]:


import numpy as np
from sklearn.cluster import KMeans
# Convert geodata into Numpy array
X = np.asarray(df_tor[['Latitude', 'Longitude']])
# K-mean Clustering
kclusters = 5
k_means = KMeans(init = "k-means++", n_clusters = kclusters, n_init = 12)
k_means.fit(X)
k_means_labels = k_means.labels_
df_tor.insert(0, 'Geo-Cluster', k_means.labels_)


# In[49]:


import folium
import matplotlib.cm as cm
import matplotlib.colors as colors
# Define latitude and longitude for Toronto
latitude = 43.651070
longitude = -79.347015
# Create map 
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)
# Set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]
# Add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(df_tor['Latitude'], df_tor['Longitude'], df_tor['Neighborhood'], df_tor['Geo-Cluster']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# In[ ]:




