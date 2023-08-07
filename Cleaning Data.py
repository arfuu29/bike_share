#!/usr/bin/env python
# coding: utf-8

# # Capstone Project Cyclistic Bike-Share

# # Cleaning Proces
# <li>Import Package</li>  
# <li>Handle Missing Value</li>
# <li>Handle duplicate data Handle irrelevant data</li>
# <li>Change the data type to match the data type</li>
# <li>Get insights from the data</li>
# <li>Export the data to a CSV file for analysis</li>
# 

# ## 1. Import Package 
# Import pandas for cleaning data <br>
# import numpy for deal with NaN data <br>
# Import matplotlib for visualize data <br>

# In[1]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# In[2]:


d_parser = lambda x: pd.datetime.strptime(x, format='%Y-%m-%d %H:%M:%S')


# In[3]:


# Import CSV File from my computer
df = pd.read_csv('Downloads/Bike-Share data/Data/cylic/bike_data.csv', date_parser=d_parser)


# In[4]:


# see row and column sizes
df.shape


# In[5]:


# Find Out Data Type every Columns
df.info()


# In[6]:


# Find out statistik about the dataset
# Find out duplicate, if there are more than two unique value on ride_id column, then there is duplicate data
df.describe()


# In[7]:


# Filter duplicate and irrelevant data
filt = df['ride_id'] == 'ride_id'


# In[8]:


df[filt]


# In[9]:


df.head(10)


# ## 2. Handle Missing Value
#    At this stage, if a row has NaN values, then that row will be deleted. This is a bad habit; NaN values should be handled better by filling values with references from other matters. But after trying the NaN values in this project, it is tough to take; most of the data has more than 5 NaN values in 1 row. This stage succeeded in deleting approximately one million data from a total of 5.8 million data. This is a bad idea.

# In[10]:


df1 = df.dropna()


# In[11]:


# Show 20 rows after deleting NaN values
df1.head(20)


# In[12]:


# Change Name Values of member_casual column
df1['member_casual'] = df1['member_casual'].replace(['member','casual'], ['annual_member', 'casual_ride'])


# In[13]:


# Cek values
df1['member_casual'].value_counts()


# In[14]:


df1.shape


# In[15]:


# Cek duplicate data
df1.describe()


# ## 3. Handle duplicate data
# In the dataset, there are duplicate data. Therefore we solve it with the drop_duplicate() function based on the ride_id column. Each row in the ride_id column must be unique because it represents one made trip.

# In[16]:


df1.drop_duplicates('ride_id', inplace=True)


# In[17]:


# Cek the dataset after drop duplicate
df1.describe()


# ## 3. Handle irrelevant data

# In[ ]:


#Cek count data use value_counts() function
df1['rideable_type'].value_counts()


# In[19]:


# Create filter
filt = df1['rideable_type'] == 'rideable_type'


# In[20]:


# Show irrelevant data
df1[filt]


# In[21]:


i = df1[(df1.ride_id == 'ride_id')].index


# In[22]:


# Drop irrelevant data
df1.drop(i, inplace=True)


# In[23]:


# Cek statistik summary
df1.describe()


# ## 4. Change the data type to match the data type
# We will convert the data type of the "started_at" and "ended_at" columns to datetime. Additionally, we will change the data type of the geo location coordinates - "start_lat", "start_lng", "end_lat", and "end_lng" - to float in order to adjust the number of decimals.

# In[24]:


# Cek column data type
df.info()


# In[25]:


# Change data type from object to datatime
df1['started_at'] = pd.to_datetime(df1['started_at'])
df1['ended_at'] = pd.to_datetime(df1['ended_at'], errors='coerce')


# In[26]:


# Change data type from object to float
df1['start_lat'] = df1['start_lat'].astype(float)
df1['start_lng'] = df1['start_lng'].astype(float)
df1['end_lat'] = df1['end_lat'].astype(float)
df1['end_lng'] = df1['end_lng'].astype(float)


# In[27]:


# Cek datatype
df1.dtypes


# ## 5. Get insights from the data

# In[29]:


count_ride_type


# In[51]:


## Insight about ride type and member type
data_count = [df1['rideable_type'].value_counts(normalize=True),df1['member_casual'].value_counts()]
for i in data_count:
    plt.figure()
    plt.style.use('ggplot')
    i.plot(kind='pie', label='')


# In[56]:


## Insight about top station start and top station end
station_data = [df1['start_station_name'].value_counts().head(10), df1['end_station_name'].value_counts().head(10)]
for i in station_data:
    plt.figure()
    plt.style.use('ggplot')
    i.plot(kind='barh')


# ## 6. Export the data to a CSV file for analysis.

# In[38]:


df1.to_csv('C:\\Users\\Huawei\\Downloads\\Bike-Share data\\Data\\cylic\\bike_share.csv', index=False)

