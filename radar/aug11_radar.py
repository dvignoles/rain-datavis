#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 14:43:56 2018

@author: Daniel Vignoles
"""

import geopandas as gpd
from radarplot import makeMaps,makeMovie,cell_series

nyc_shp = '/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/shp/nybb_18c/nybb.shp'

rast = '/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/radar/aug11/select_geotiff'

out = '/Users/user/Desktop/DANIEL_VIGNOLES/Fall2018/radar/aug11/plt_out'

nyc = gpd.read_file(nyc_shp)
nyc = nyc.to_crs(epsg = 4326)

#makeMaps(rast, out, nyc)
#makeMovie('radar_aug11',out,1)

                #lat            #lon
asrc = (40.81564962581866,-73.95024781009221)

asrc_aug11 = cell_series(rast,asrc[1],asrc[0])