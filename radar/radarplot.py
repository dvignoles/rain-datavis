#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 10:27:11 2018

@author: Daniel Vignoles

#For use with Raster images from NOAA NEXRAD Radar Kokx Station
"""

import rasterio
from rasterio.plot import show
from rasterio.transform import xy,rowcol
import matplotlib.pyplot as plt
import os
import datetime as dt
import imageio

def makeMaps(rast_dir, out_dir, basemap):
    """
        rast_dir -- directory containing raster images,
        out_dir -- directory to output images to
        basemap -- GeoDataFrame to use as base map for images
    
    """
    for filename in os.listdir(rast_dir):
        ax = basemap.plot(alpha = 0.75, color = 'b')
        #CRS({'init': 'epsg:4326'})
        data = rasterio.open(rast_dir + '/' + filename)
        
        plt.ioff() #turn off interactive plot popups
        show(data,ax = ax, with_bounds = True, cmap = 'YlOrRd')
        
        ax.set_xbound(basemap.total_bounds[0],basemap.total_bounds[2])
        ax.set_ybound(basemap.total_bounds[1],basemap.total_bounds[3])
        
        date_str = filename[9:-4]
        date = dt.datetime.strptime(date_str,'%Y%m%d_%H%M%S')
        date_str = dt.datetime.strftime(date,'%c')
        ax.set_title('Dual Pol Radar NYC ' + date_str)
        
        fname = out_dir + '/' + filename[:-4] + '.png'
        plt.savefig(fname)
        plt.close('all')
    

def makeMovie(name, out_dir, fps):
    """
        name -- filename 
        out_dir -- directory to output mp4 file
        fps -- frames per second of movie
    """
    writer = imageio.get_writer(out_dir + '/' + name + '.mp4', fps=fps)

    for fname in os.listdir(out_dir):
        if fname.endswith('.png'):
            writer.append_data(imageio.imread(out_dir + '/' +fname))
    writer.close()
    
    
def cell_series(rast_dir, lon, lat):
    """
        get the values of a particular latitude longitude in a time series of rasters
    """
    
    cell_series = []
    
    with rasterio.open(rast_dir + '/' + os.listdir(rast_dir)[0]) as data:
    
        aff = data.transform
        
        row,col = rowcol(aff,lon,lat)
        
        for fname in os.listdir(rast_dir):
            with rasterio.open(rast_dir + '/' + fname) as rast:
                vals = rast.read()
                val_at_coord = vals[0,row,col]
                date_str = fname[9:-4]
                date = dt.datetime.strptime(date_str,'%Y%m%d_%H%M%S')
                cell_series.append((date,val_at_coord))
        
    return(cell_series)
                
                
                
        
    

