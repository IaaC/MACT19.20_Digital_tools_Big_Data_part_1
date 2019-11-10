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
import matplotlib.pyplot as plt
import glob
import urllib.request
import json
import time
from key import routing_key

# We read all csv.zop files within the filder and merge them into a single dataframe
path = '../data/citibike'                       # This is the path to our files
all_files = glob.glob(path + "/*.csv.zip")
top_value = 1000

records_month = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    records_month.append(df)
trips = pd.concat(records_month, axis=0, ignore_index=True)


# We group trips by start/end station and count the number of trips happening between these stations
count_trips = trips.groupby(['start station id', 'start station latitude', 'start station longitude',
                             'end station id', 'end station latitude', 'end station longitude'], as_index=False)
count_trips = count_trips['bikeid'].count()
count_trips.columns = ['start_id', 'start_lat', 'start_lon', 'end_id', 'end_lat', 'end_lon', 'total_trips']

# We can get only the routes where most of the trips have happened
top_routes = count_trips.nlargest(top_value, 'total_trips')


# Now we set the URL for using the API, we need a key and two pairs of coordinates
base_url = 'https://api.openrouteservice.org/v2/directions/%s?api_key=%s&start=%f,%f&end=%f,%f'
profile = 'cycling-regular'            # Alternatives are car | bike | foot
key = routing_key.ors_key    # get yours here https://openrouteservice.org

# We set and empty list to store every single route after
features = []

# Using a loop, we use the API to get the shortes path and append the start/end stations and the number of trips
for i_s, route in top_routes.iterrows():
    if route['start_id'] == route['end_id']:
        # This conditional prevents from calculating routes having the same start/end station
        print('Error: start/end stations equal: %s' % str(route['start_id']))
    else:
        url = base_url % (profile, key, route['start_lon'], route['start_lat'], route['end_lon'], route['end_lat'])
        try:
            # This structure prevents from errors when using this API (internet connection or format errors)
            with urllib.request.urlopen(url) as request:
                s = request.read()
            print(s)
            gdf = geopandas.GeoDataFrame.from_features(json.loads(s)['features'])
            summary = gdf['summary']
            gdf['distance'] = summary[0]['distance']
            gdf['duration'] = summary[0]['duration']
            gdf['start_id'] = route['start_id']
            gdf['end_id'] = route['end_id']
            gdf['total_trips'] = route['total_trips']
            gdf = gdf[['start_id', 'end_id', 'total_trips', 'geometry', 'distance', 'duration']]
            features.append(gdf)
            time.sleep(2)
        except:
            print('Error in API request')

# Now we group or concatenate all the routes calculated into a GeoDataframe. It is stored into a File
routes = geopandas.GeoDataFrame(pd.concat(features, ignore_index=True), crs=features[0].crs)
routes.plot()
plt.show()
routes.to_file('../outcomes/citibike_top_routes.geojson', driver="GeoJSON")


# Here there are some suggestions for future analysis
# Route per bicycle,
# Route per day
