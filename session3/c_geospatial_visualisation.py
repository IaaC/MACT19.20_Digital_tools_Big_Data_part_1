# encoding: utf-8

##################################################
# This script shows uses the pandas library to create statistically describe datasets
# It also shows basic plotting features
# Find extra documentation about data frame here:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
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
import mapclassify
import pyproj
from pyproj import Proj

# We read the file for population data
countries = geopandas.read_file('../data/world/ne_admin_0_countries.geojson')
pop = pd.read_csv('../data/world/pop_total_v2.csv', skiprows=4, header=0)
gdp = pd.read_csv('../data/world/gdp_percap_v2.csv', skiprows=4, header=0)

# PRINT OUT a basic plot with countries
ax = countries.plot()
ax.set_title("World map")
plt.show()

# Merging data and plotting two elements
# prepare population data, merge with countries data frame and get a subset of columns

# EXTRACT COLUMNS 'COUNTRY CODE' AND '1960' FROM THE DATAFRAME POP (: MEANS THAT I EXTRACT ALL THE ROWS)
pop_1960 = pop.loc[:, ['Country Code', '1960']]
# MERGE THE TWO DATAFRAMES 'COUNTRIES' AND 'POP_1960'
countries_pop_1960 = pd.merge(countries, pop_1960, left_on='ADM0_A3', right_on='Country Code', how='left')
countries_pop_1960 = countries_pop_1960[['ADM0_A3', 'NAME', 'geometry', 'Country Code', '1960']].dropna()
# Set up the visual outputs using subplots for map and legend elements
fig, ax = plt.subplots(1, 1)
# Additional schemas come from "mapclassify" library
countries_pop_1960.plot(column='1960', ax=ax, cmap='magma', scheme='fisher_jenks', legend=True)
ax.set_title("World Population. Year 1960")
ax.set_axis_off()
plt.show()
# There are options for saving plots
# plt.savefig('../outcomes/map_pop.png', dpi=300, format='png')


# How about multiple plots
# prepare population data, merge with countries data frame and get a subset of columns

# EXTRACT DIFFERENT COLUMNS FROM THE GDP DATAFRAME (: MEANS I EXTRACT ALL THE ROWS)
gdp_years = gdp.loc[:, ['Country Code', '1960', '1980', '2000', '2018']]
# MERGE THE TWO DATAFRAMES 'COUNTRIES' AND 'GDP_YEARS'
countries_gdp = pd.merge(countries, gdp_years, left_on='ADM0_A3', right_on='Country Code', how='left')
# EXTRACT DIFFERENT COLUMNS FROM THE COUNTRIES_GDP DATAFRAME (fill.na(0) IS USED TO REPLACE ALL THE NAN VALUES WITH 0)
countries_gdp = countries_gdp[['ADM0_A3', 'NAME', 'geometry', 'Country Code', '1960', '1980', '2000', '2018']].fillna(0)
# SET UP THE VISUAL OUTPUT
fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
# SET THE FIRST MAP
countries_gdp.plot(column='1960', ax=ax1, cmap='magma', scheme='fisher_jenks', legend=False)
ax1.set_axis_off()
# SET THE SECOND MAP
countries_gdp.plot(column='1980', ax=ax2, cmap='magma', scheme='fisher_jenks', legend=False)
ax2.set_axis_off()
# SET THE THIRD MAP
countries_gdp.plot(column='2000', ax=ax3, cmap='magma', scheme='fisher_jenks', legend=False)
ax3.set_axis_off()
# SET THE FOURTH MAP
countries_gdp.plot(column='2018', ax=ax4, cmap='magma', scheme='fisher_jenks', legend=True)
ax4.set_axis_off()
ax.set_axis_off()
plt.show()
# There are options for saving plots
# plt.savefig('../outcomes/map_gdp.png', dpi=300, format='png')

# Now for Antarctica and the well-known issues of cartographic projections
print('Countries data is originally stored in ')
# PRINT THE COORDINATE REFERENCE SYSTEM ATTRIBUTE
print(countries.crs)
antarctica = countries[countries['NAME'] == 'Antarctica']

# CHANGE COORDINATES REFERENCE SYSTEM FROM 4326 TO 3031 (IMPORTANT TO INSTALL PYPROJ LIBRARY VERSION 2.2.0)
antarctica = antarctica.to_crs({'init': 'epsg:3031'})
ax = antarctica.plot()
ax.set_title("Antarctica")
plt.show()
