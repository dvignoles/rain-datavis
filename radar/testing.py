#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:36:19 2018

@author: user
"""

import rasterio
from rasterio.transform import xy,rowcol


data = rasterio.open('/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/radar/aug11/select_geotiff/KOKX_DAA_20180811_050300.tif')

bb = data.bounds
west = bb.left
south = bb.bottom
east = bb.right
north = bb.top

width = data.width
height = data.height

aff = data.transform


raw = data.read()
                #lat            #lon
asrc_coord = (40.81564962581866,-73.95024781009221)

#rowcol returns row and column of(x,y) in a given crs
r,c = rowcol(aff,asrc_coord[1],asrc_coord[0])

#return x,y coord from row,col index of data
x,y = xy(aff,r,c)
