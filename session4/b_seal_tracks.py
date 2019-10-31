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

countries = geopandas.read_file('../data/world/ne_admin_0_countries.geojson')
seal_tracks = geopandas.read_file('../data/world/MEOP_SealTracks.geojson')


# We can plot individual layers
countries.plot()
plt.show()
seal_tracks.plot()
plt.show()


# However, if we want to combine them, it is a good idea to use base layers
# We need to be sure the layers have compatible crs
antarctica = countries[countries['NAME'] == 'Antarctica']
antarctica = antarctica.to_crs({'init': 'epsg:3031'})
base = antarctica.plot(color='gray', edgecolor='white')
base.set_axis_off()
seal_tracks.plot(ax=base, linewidth=0.05)
plt.show()


# We can also use loops for creating maps depending on a variable
# The seal tracks layer has a year in which the line was recorded (check the metadata to confirm this)
years = seal_tracks['year'].unique()
for y in years:
    # We set the base map, remove the axis labels and set a fix extent for each map
    base = antarctica.plot(color='black', edgecolor='white')
    base.set_axis_off()
    plt.ylim(-5000000, 5000000)
    plt.xlim(-6000000, 6000000)
    plt.title('Seal tracks year %s' % y)  # Here we add a customised title
    seal_tracks[seal_tracks['year'] == y].plot(ax=base, color='gray', linewidth=0.07)
    file = '../outcomes/seal_tracks_%s.png' % y  # Every single map is saved
    plt.savefig(file, dpi=300, format='png')
    plt.close()
    print('Seal tracks map for year %s saved' % y)

# Try to add some other data sets to this map
