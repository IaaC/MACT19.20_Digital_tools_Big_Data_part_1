# encoding: utf-8

##################################################
# This script shows additional options to define plots (bar, stacked bars, etc.)
# GIS more user-friendly options but having the option for using loops and conditionals might serve for simple tasks
# Find extra documentation about seaborn plots:
# https://seaborn.pydata.org/examples/color_palettes.html
# https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
# https://seaborn.pydata.org/examples/heatmap_annotation.html
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

# We need to import pandas, matplotlib, seaborn and numpy libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np

# We load the data and sort it considering the max_capacity column
facilities_all = pd.read_csv('../data/antarctica/COMNAP_Antarctic_Facilities.csv')
facilities = facilities_all[facilities_all['max_cap'] > 0]
facilities = facilities.sort_values(['max_cap'], ascending=False).reset_index(drop=True)

# Setting the style from seaborn gallery. Che
sns.set(style="white")
sns.set_color_codes("pastel")


# Set up the matplotlib figure
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 5), sharey=True)

# Generate some sequential data
sns.barplot(x='max_cap', y='name_eng',  label="Max. Capacity", color='gray', ax=ax1, data=facilities)
sns.barplot(x='avg_pop_wn', y='name_eng',  label="Avg. Pop. Winter", color='b', ax=ax1, data=facilities)
sns.barplot(x='max_cap', y='name_eng',  label="Max. Capacity", color='gray', ax=ax2, data=facilities)
sns.barplot(x='avg_pop_sm', y='name_eng',  label="Avg. Pop. Winter", color='r', ax=ax2, data=facilities)
ax1.set_xlabel("Winter Population vs. Capacity")
ax1.set_ylabel("")
ax1.tick_params(labelsize=6)
ax2.set_xlabel("Summer Population vs. Capacity")
ax2.set_ylabel("")
plt.show()


# Data stored in columns also serve for creating facets to split out plots, it can be either 1 or 2 dimension facets
facilities['peak_ocu'] = facilities['peak_pop'] / facilities['max_cap'] * 100
g = sns.FacetGrid(facilities, col='ant_reg')
g = g.map(sns.barplot, 'name_eng', 'peak_ocu', color='gray')
g.set_titles("{col_name}")
g.set(ylabel='Peak occupation (%)', xlabel='')
plt.show()


# Heat maps are also an alternative to visualise patters. We can use it to represent the number of stations
# stablished per regions and years. It implies operations of aggregation and count

# It creates a simplified dataframe with integer values as well as a pivot table for the counting function
facilities_region = facilities_all[['ant_reg', 'year_est', 'max_cap']]
facilities_region = facilities_region.dropna()
# Changing year values from float to integer
facilities_region['year_est'] = facilities_region['year_est'].apply(lambda x: int(x) if x == x else '')
facilities_region = facilities_region.groupby(by=['ant_reg', 'year_est'], as_index=False).count()
facilities_region = facilities_region.pivot('ant_reg', 'year_est', 'max_cap')

# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots()
sns.heatmap(facilities_region, annot=True, linewidths=.5, ax=ax, cbar=False)
plt.xlabel('')
plt.ylabel('')
plt.title('New stations established per year')
plt.show()

print('Done')





