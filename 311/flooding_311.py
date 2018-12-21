#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:52:42 2018
Data Visualization of Geolocated 311 Data retrieved from NYC socrata, filtered by 'flooding'
@author: Daniel Vignoles
"""

#https://medium.com/@chrieke/essential-geospatial-python-libraries-5d82fcc38731
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
#import contextily as ctx
import matplotlib.pyplot as plt

#MAC
#aug11_file = '/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/nyc311/aug_11.csv'
#july17_file = '/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/nyc311/july_17.csv'
#sep19_file = '/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/nyc311/sep_19.csv'

#WINDOWS
july17_6_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\july17_6hour.csv"
july17_12_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\july17_12hour.csv"
july17_24_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\july17_24hour.csv"

aug11_6_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\aug11_6hour.csv"
aug11_12_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\aug11_12hour.csv"
aug11_24_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\aug11_24hour.csv"

sep18_6_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\sep18_6hour.csv"
sep18_12_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\sep18_12hour.csv"
sep18_24_file = "C:\\Users\\dvign\\Desktop\\asrc\\Fall2018\\nyc311\\sep18_24hour.csv"

#Columns to keep from csv
keep = ['Created Date','Descriptor','Incident Address','Borough','Latitude','Longitude']

def dfProcess(fname):
    df = pd.read_csv(fname, header = 0, parse_dates = True, index_col = 0)
    df = df[keep]
    df = df.dropna(axis = 'index',subset = ['Latitude','Longitude'])
    df['Coordinates'] = list(zip(df.Longitude,df.Latitude))
    df['Coordinates'] = df['Coordinates'].apply(Point)
    df = gpd.GeoDataFrame(df, geometry = 'Coordinates')
    df.crs = {'init' :'epsg:4326'}
    return df

july17_6h = dfProcess(july17_6_file)
july17_12h = dfProcess(july17_12_file)
july17_24h = dfProcess(july17_24_file)

aug11_6h = dfProcess(aug11_6_file)
aug11_12h = dfProcess(aug11_12_file)
aug11_24h = dfProcess(aug11_24_file)

sep18_6h = dfProcess(sep18_6_file)
sep18_12h = dfProcess(sep18_12_file)
sep18_24h = dfProcess(sep18_24_file)

nyc = gpd.read_file("C:\\Users\\dvign\\Desktop\\asrc\\shp\\nybb_18c\\nybb.shp")
nyc = nyc.to_crs(epsg = 4326)

#Weather Stations
station_loc = pd.DataFrame({'Station':['Laguardia','Central Park','JFK'],
                            'Latitude':[40.7792,40.77898,40.6386],
                            'Longitude':[-73.88,-73.96925,-73.7622]})
    
station_loc['location'] = list(zip(station_loc.Longitude,station_loc.Latitude))
station_loc['location'] = station_loc['location'].apply(Point)
station_loc = gpd.GeoDataFrame(station_loc, geometry = 'location')
station_loc.crs = {'init' :'epsg:4326'}

key = ['24 hours', '12 hours', '6 hours', 'Weather Stations']
def plot( df_24h,  df_12h, df_6h, title):
    ax = nyc.plot(alpha = 0.5)
    df_24h.plot(ax = ax, color = 'g')
    df_12h.plot(ax = ax, color = 'b')
    df_6h.plot(ax = ax, color = 'r')
    
    station_loc.plot(ax = ax, marker = '*', c = 'k', markersize = 256)
    
    plt.rcParams.update({'font.size': 16})
    ax.tick_params(bottom = False, left = False, labelbottom = False, labelleft = False)
    ax.set_title(title)
    ax.legend(key,prop={'size': 24})
    
    fig = plt.gcf()
    fig.suptitle('\"Flooding\" Related 311 Calls' ,fontsize=24)
    fig.set_size_inches(fig.get_size_inches() * 2.5)
    return fig


july17_title = 'July 17 02:00PM'
f = plot(july17_24h, july17_12h, july17_6h, july17_title)
f.savefig('july17_b_311')

aug11_title = 'August 11 08:00AM'
f = plot(aug11_24h, aug11_12h, aug11_6h, aug11_title)
f.savefig('aug11_b_311')

sep18_title = 'September 18 12:00PM'
f = plot(sep18_24h, sep18_12h, sep18_6h, sep18_title)
f.savefig('sep18_b_311')








