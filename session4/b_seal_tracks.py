# encoding: utf-8

##################################################
# This script shows basic mapping tools using geopandas. It serves as an example for algorithmic mapping
# GIS more user-friendly options but having the option for using loops and conditionals might serve for simple tasks
# Find extra documentation about mapping with geopandas here:
# http://geopandas.org/mapping.html#maps-with-layers
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

# We need to import pandas library
import geopandas
import matplotlib.pyplot as plt

# create geodataframes reading the geopandas files
countries = geopandas.read_file('../data/world/ne_admin_0_countries.geojson')
seal_tracks = geopandas.read_file('../data/world/MEOP_SealTracks.geojson')

# We can plot individual layers
# plot just countries
countries.plot()
plt.show()
# plot just seal tracks
seal_tracks.plot()
plt.show()

# However, if we want to combine them, it is a good idea to use base layers
# We need to be sure the layers have compatible crs (coordinates reference system)

# extract the Antarctica row from the name column
antarctica = countries[countries['NAME'] == 'Antarctica']
# this line is to check the crs
antarctica = antarctica.to_crs({'init': 'epsg:3031'})
# set antarctica plot
base = antarctica.plot(color='gray', edgecolor='white')
# remove base axis
base.set_axis_off()
# set seal tracks plot
st = seal_tracks.plot(ax=base, linewidth=0.05)
# remove st axis
st.set_axis_off()
# show plots
plt.show()

# We can also use loops for creating maps depending on a variable
# The seal tracks layer has a year in which the line was recorded (check the metadata to confirm this)

# this line sorts all the values (not mandatory, the script works anyway)
years = seal_tracks['year'].sort_values()
# this line groups all the same years
years = years.unique()
# for loop iteration to go through every year
for y in years:
    # if y = 'None' the value is skipped
    if y is None:
        continue
    # We set the base map, remove the axis labels and set a fix extent for each map
    base = antarctica.plot(color='black', edgecolor='white')
    base.set_axis_off()
    plt.ylim(-5000000, 5000000)
    plt.xlim(-6000000, 6000000)
    # set plot title (%s will be replaced each time by the year (y)
    plt.title('Seal tracks year %s' % y)  # Here we add a customised title
    # if the year of the seal tracks geodataframe is equal to y then set the plot
    seal_tracks[seal_tracks['year'] == y].plot(ax=base, color='gray', linewidth=0.07)
    # save each image in the outcomes folder
    file = '../outcomes/seal_tracks_%s.png' % y  # the extension needs to be the same as the format of the line below
    # set the definition and format of the images (there are different options for formats e.g. png, pdf, etc)
    # for formats look at documentation here (https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.savefig.html)
    plt.savefig(file, dpi=300, format='png')
    plt.close()
    # print this string each time that a seal track map is saved
    print('Seal tracks map for year %s saved' % y)

# Try to add some other data sets to this map
