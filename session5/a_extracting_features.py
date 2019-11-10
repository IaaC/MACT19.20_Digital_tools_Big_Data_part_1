# encoding: utf-8

##################################################
# This script uses the pandas library to create new indicators from original datasets
# It also shows basic plotting features
# Get NYC data from:
# Find extra documentation about data frame operations here:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html

##################################################
#
##################################################
# Author: Diego Pajarito
# Copyright: Copyright 2019, IAAC
# Credits: [Institute for Advanced Architecture of Catalonia - IAAC, Advanced Architecture group]
# License:  Apache License Version 2.0
# Version: 1.0.0
# Maintainer: Diego Pajarito
# Email: diego.pajarito@iaac.net
# Status: development
##################################################

# We need to import pandas library as well as the plot libraries matplotlib and seaborn
import pandas as pd
import geopandas
from shapely.geometry import Point
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import glob

# We read all csv.zop files within the filder and merge them into a single dataframe
path = '../data/citibike'                       # This is the path to our files
all_files = glob.glob(path + "/*.csv.zip")

records_month = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    records_month.append(df)
trips = pd.concat(records_month, axis=0, ignore_index=True)


# We can use different aggregation functions to better represent spatial dimensions of our data
# Function count. We group trips by station for extracting stations and also get aggregated values
# total number of trips per station
stations_count = trips.groupby(['start station id', 'start station name',
                          'start station latitude', 'start station longitude'], as_index=False)
stations = stations_count['bikeid'].count()

# trips per station and user type
stations_user = trips.groupby(['start station id', 'start station name',
                          'start station latitude', 'start station longitude', 'usertype'], as_index=False)
stations_user = stations_user['bikeid'].count()
stations_user_customer = stations_user.loc[stations_user['usertype'] == 'Customer', ['start station id', 'bikeid']]
stations_user_customer.columns = ['start station id', 'trips_customers']
stations = pd.merge(stations, stations_user_customer, how='left')
stations_user_subscriber = stations_user.loc[stations_user['usertype'] == 'Subscriber', ['start station id', 'bikeid']]
stations_user_subscriber.columns = ['start station id', 'trips_subscriber']
stations = pd.merge(stations, stations_user_customer, how='left')

# trips per station and gender
stations_gender = trips.groupby(['start station id', 'start station name',
                          'start station latitude', 'start station longitude', 'gender'], as_index=False)
stations_gender = stations_gender['bikeid'].count()
stations_gender_u = stations_gender.loc[stations_gender['gender'] == 0, ['start station id', 'bikeid']]
stations_gender_u.columns = ['start station id', 'trips_gender_u']
stations = pd.merge(stations, stations_gender_u, how='left')
stations_gender_m = stations_gender.loc[stations_gender['gender'] == 1, ['start station id', 'bikeid']]
stations_gender_m.columns = ['start station id', 'trips_male']
stations = pd.merge(stations, stations_gender_m, how='left')
stations_gender_f = stations_gender.loc[stations_gender['gender'] == 2, ['start station id', 'bikeid']]
stations_gender_f.columns = ['start station id', 'trips_female']
stations = pd.merge(stations, stations_gender_f, how='left')


# Function average. Average trip duration and user birth year
stations_average = trips.groupby(['start station id', 'start station name',
                                  'start station latitude', 'start station longitude'], as_index=False)
stations_average = stations_average['tripduration', 'birth year'].mean()
stations_average = stations_average[['start station id', 'tripduration', 'birth year']]
stations_average.columns = ['start station id', 'trip_duration', 'avg_age']
stations_average['avg_age'] = 2019 - round(stations_average['avg_age'])
stations = pd.merge(stations, stations_average, how='left')


# Function mode. Most prefered end estation
stations_mode = trips.groupby(['start station id', 'start station name',
                               'start station latitude', 'start station longitude'], as_index=False)
stations_mode = stations_mode['end station id'].agg(pd.Series.mode)
stations_mode = stations_mode[['start station id', 'end station id']]
stations_mode['end station id'] = str(stations_mode['end station id'])  # Mode function can return multiple values
stations = pd.merge(stations, stations_mode, how='left')

# Finally we merge all the results into a single data frame and turn it into a geodataframe
stations.columns = ['station_id', 'station_name', 'lat', 'lon', 'total_trips_o', 'trip_costumers', 'trips_gender_u',
                    'trips_male', 'trips_female', 'trip_duration', 'avg_age', 'end_station_mode']

stations_geo = GeoDataFrame(stations, crs={'init': 'epsg:4326'},
                            geometry=[Point(xy) for xy in zip(stations.lon, stations.lat)])
stations_geo.to_file('../outcomes/citibike_stations.geojson', driver="GeoJSON")
stations_geo.plot()


