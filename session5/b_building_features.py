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
import urllib.request
import json
from key import routing_key

# We read all csv.zop files within the filder and merge them into a single dataframe
path = '../data/citibike'                       # This is the path to our files
all_files = glob.glob(path + "/*.csv.zip")

records_month = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    records_month.append(df)
trips = pd.concat(records_month, axis=0, ignore_index=True)


# We group trips by station for extracting stations and building up a single geojson file
stations = trips.groupby(['start station id', 'start station name',
                          'start station latitude', 'start station longitude'], as_index=False)
stations = stations['bikeid'].count()
stations.columns = ['station_id', 'station_name', 'lat', 'lon', 'total_trips_o']

test_ids = [293, 402, 465, 468] # This are random stations chosen for the explanation
stations = stations[stations['station_id'].isin(test_ids)]


# Shortest path OSM
base_url = 'https://api.openrouteservice.org/v2/directions/%s?api_key=%s&start=%f,%f&end=%f,%f'
profile = 'cycling-regular'            # Alternatives are car | bike | foot
key = routing_key.ors_key    # get yours here https://openrouteservice.org

# We create a list for storing all routes after calculated
features = []

for i_s, start in stations.iterrows():
    for i_e, end in stations.iterrows():
        # We use two loops to go trough the combination of coordinates to combine all possible routes between stations
        if start['station_id'] != end['station_id']:
            # This conditional prevents from calculating routes when start/end stations are equal
            url = base_url % (profile, key, start['lon'], start['lat'], end['lon'], end['lat'])
            print(url)
            try:
                # This structure prevents from errors when using this API (internet connection or format errors)
                with urllib.request.urlopen(url) as request:
                    s = request.read()
                print(s)
                gdf = geopandas.GeoDataFrame.from_features(json.loads(s)['features'])
                summary = gdf['summary']
                gdf['distance'] = summary[0]['distance']
                gdf['duration'] = summary[0]['duration']
                gdf['station_start'] = start['station_id']
                gdf['station_end'] = end['station_id']
                gdf = gdf[['geometry', 'distance', 'duration']]
                features.append(gdf)
            except:
                print('Error in API request')

# Here we group all the calculated routes into a Geodataframe and store it into a file
routes = geopandas.GeoDataFrame(pd.concat(features, ignore_index=True), crs=features[0].crs)
routes.to_file('../outcomes/citibike_shortest_path.geojson', driver="GeoJSON")
routes.plot()
plt.show()

# Route per bicycle,
# Route per day
# Shortest path OSM
