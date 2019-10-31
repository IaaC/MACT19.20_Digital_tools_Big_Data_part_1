# encoding: utf-8

##################################################
# This script uses the pandas library to create new indicators from original datasets
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
import seaborn as sns

# We read the file for population and gdp data. Also geospatial data about countries
population = pd.read_csv('../data/world/pop_total_v2.csv', skiprows=4, header=0)
gdp = pd.read_csv('../data/world/gdp_percap_v2.csv', skiprows=4, header=0)
countries = geopandas.read_file('../data/world/ne_admin_0_countries.geojson')

# Since the data combines information from countries and regions, we need to split out the two levels based on the list
regions_list = ['Central Europe and the Baltics', 'Caribbean small states',
                'East Asia & Pacific (excluding high income)', 'Early-demographic dividend', 'East Asia & Pacific',
                'East Asia & Pacific', 'Europe & Central Asia (excluding high income)', 'Europe & Central Asia',
                'Euro area', 'European Union', 'Fragile and conflict affected situations',
                'Heavily indebted poor Countries (HIPC)', 'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only',
                'Non classified', 'Latin America & Caribbean (excluding high income)',
                'Latin America & Caribbean', 'Least developed countries: UN classification',
                'Low Income', 'Lower middle income', 'Low & middle income', 'Late-demographic dividend',
                'Middle East & North Africa', 'Middle income', 'Middle East & North Africa (excluding high income)',
                'North America', 'OECD members', 'Other small states', 'Pre-demographic dividend',
                'Pacific island small states', 'Post-demographic dividend',
                'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa', 'Small states',
                'East Asia & Pacific (IDA & IBRD countries', 'Europe & Central Asia (IDA & IBRD countries)',
                'Latin America & the Caribbean (IDA & IBRD countries)',
                'Middle East & North Africa (IDA & IBRD countries', 'South Asia (IDA & IBRD)',
                'Sub-Saharan Africa (IDA & IBRD countries)', 'Upper middle income', 'World']
# This time we are only working with country data
pop_regions = population[~population['Country Name'].isin(regions_list)]
gdp_regions = gdp[~gdp['Country Code'].isin(regions_list)]
growth = pd.DataFrame(columns=['Country Code', 'year', 'growth'])

# Population growth lines
for year in range(1960, 2018):
    value_pop = pop_regions[['Country Code', str(year), str(year + 1)]]
    # use population growth formula
    value_pop['growth'] = (value_pop[str(year + 1)] - value_pop[str(year)]) / value_pop[str(year)] * 100
    value_pop['year'] = year
    # then we create an empty dataframe and append the three columns 'country code' 'growth' 'year'
    growth = growth.append(value_pop[['Country Code', 'growth', 'year']])
    print('Added calculations for year %i' % year)

# create a line plot with x axis 'year' and y axis 'growth'
ax = sns.lineplot(x='year', y='growth', hue='Country Code', data=growth, legend=False)
# show plot
plt.show()


# For the following tasks we need a simplified geodataframe for countries. Only country code and geometry is needed
countries = countries[['ADM0_A3', 'geometry']]
countries.columns = ['Country Code', 'geometry']


# We can also apply a "Group by" function to calculate averages or other summary statistics
# This functions serves to simplify data and to generate new data sets
avg_growth = growth.groupby(by=['Country Code']).mean()     # Mind the difference added by the parameter "as_index"
avg_growth = growth.groupby(by=['Country Code'], as_index=False).mean()
# We can merge the results with geospatial information and map it
countries_pop_avg_growth = countries.merge(avg_growth, on='Country Code')
countries_pop_avg_growth.plot(column='growth', legend='true')
plt.show()


# Using the new data we can export this result for visualisation in GIS
# We can use the geojson file

countries_pop_growth = countries.merge(growth, on='Country Code', how='right')
countries_pop_growth.to_file('../outcomes/pop_growth')
print('Shapefile Saved...')

# Try to visualise population growth map with three categories (< -1.5 | -1.5 to 1.5 | > 1.5)

