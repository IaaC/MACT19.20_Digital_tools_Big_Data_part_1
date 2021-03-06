# encoding: utf-8

##################################################
# This script shows uses the pandas library to create personalised plots that support descriptive analytics
# It uses mainly the seaborn library and its basic features
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
import seaborn as sns;

sns.set()
import matplotlib.pyplot as plt
import numpy as np

# We read the file for population data
population = pd.read_csv('../data/world/pop_total_v2.csv', skiprows=4, header=0)
gdp = pd.read_csv('../data/world/gdp_percap_v2.csv', skiprows=4, header=0)

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

# first select the dataframe columns and then filter the names according to the regions_list
pop_regions = population[population['Country Name'].isin(regions_list)]
gdp_regions = gdp[gdp['Country Name'].isin(regions_list)]

# make scatter plots
ax = sns.scatterplot(x=pop_regions['2018']/1000000000, y=gdp_regions['2018']/1000)
ax = sns.scatterplot(x=pop_regions['2010']/1000000000, y=gdp_regions['2010']/1000)
plt.xlabel('Population (Billions)')
plt.ylabel('GDP (Thousands of USD)')
plt.show()

# We can select a shorter list and use color to differentiate between the regions
regions_list = ['Central Europe and the Baltics', 'Caribbean small states', 'East Asia & Pacific',
                'Europe & Central Asia', 'Latin America & Caribbean', 'Middle East & North Africa',
                'North America', 'Pacific island small states', 'Sub-Saharan Africa', 'South Asia']

# first select the dataframe columns and then filter the names according to the regions_list
pop_regions = population[population['Country Name'].isin(regions_list)]
gdp_regions = gdp[gdp['Country Name'].isin(regions_list)]

# make the scatter plots
ax = sns.scatterplot(x=pop_regions['2018']/1000000000, y=gdp_regions['2018']/1000, hue=pop_regions['Country Name'])
ax = sns.scatterplot(x=pop_regions['2010']/1000000000, y=gdp_regions['2010']/1000, hue=pop_regions['Country Name'],
                     legend=False)
ax = sns.scatterplot(x=pop_regions['2000']/1000000000, y=gdp_regions['2000']/1000, hue=pop_regions['Country Name'],
                     legend=False)
# set scatterplot title
plt.title('World regions - years: 2000, 2010 and 2018')
# set scatter plot x label
plt.xlabel('Population (Billions)')
# set scatter plot y label
plt.ylabel('GDP (Thousands of USD)')
# show plot
plt.show()

# Scatter plot population vs gdp for a single country + Legend + Colors  2018
la_list = ['Argentina', 'Antigua and Barbuda', 'Bahamas, The', 'Belize', 'Bermuda',
           'Bolivia', 'Brazil', 'Barbados', 'Cuba', 'Curacao', 'Cayman Islands', 'Dominica', 'Dominican Republic',
           'Ecuador', 'Guatemala', 'Guyana', 'Honduras', 'Haiti', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Peru',
           'Puerto Rico', 'Paraguay', 'El Salvador', 'Uruguay', 'St. Vincent and the Grenadines', 'Venezuela, RB',
           'British Virgin Islands', 'Virgin Islands (U.S.)']
pop_regions = population[population['Country Name'].isin(la_list)]
gdp_regions = gdp[gdp['Country Name'].isin(la_list)]
# set mean value of pop_regions dataframe column '2018'
mean_pop = pop_regions['2018'].mean()/1000000
# set mean value of gdp_regions dataframe column '2018'
mean_gdp = gdp_regions['2018'].mean()/1000
# set scatterplot
ax = sns.scatterplot(x=pop_regions['2018']/1000000, y=gdp_regions['2018']/1000, hue=pop_regions['Country Code'])
# set scatterplot legend
plt.legend(loc='upper right', frameon=False, ncol=5, fontsize=6)
plt.axhline(mean_gdp, ls='--')
plt.axvline(mean_pop, ls='--')
# set scatterplot title
plt.title('Latin America & Caribbean - 2018')
# set scatterplot xlabel
plt.xlabel('Population (Millions)')
# set scatterplot xlabel
plt.ylabel('GDP (Thousands of USD)')
# show scatterplot
plt.show()

# Animation for the regions
# for loop that goes from the 1960 year to the 2018 one
for year in range(1960, 2018):
    # % simbol will be replaced each time by the year value
    title = 'Latin America & Caribbean. Population vs. GDP. Year %i' % year
    file = '../outcomes/frame_%i.png' % year
    # scatterplot iteration that produces all the correlation graphs in a row
    ax = sns.scatterplot(x=pop_regions[str(year)] / 1000000, y=gdp_regions[str(year)] / 1000, size=0.1,
                         hue=pop_regions['Country Code'], legend=False)
    # define the y limit
    plt.ylim(-1, 50)
    # define the y limit
    plt.xlim(-3, 220)
    # add title
    plt.title(title)
    # add x label
    plt.xlabel('Population (Millions)')
    # add y label
    plt.ylabel('GDP (Thousands of USD)')
    # save the scatterplots in png format
    plt.savefig(file, dpi=300, format='png')
    plt.close()
    print('Saved plot for year: %i' % year)

print('done')
