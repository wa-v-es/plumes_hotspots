#awk '{seen[$3]} END {print length(seen)}' arrSta_eq2_1.5.txt
import matplotlib.pyplot as plt
import numpy as np
import obspy
from obspy import read, Stream, UTCDateTime,read_events
from obspy.core.event import Origin
from obspy.clients.fdsn import Client
import os
import cartopy.crs as ccrs
import sys
import cartopy.feature as cfeature
import requests
from obspy.taup.taup_geo import calc_dist,calc_dist_azi


class Stations:
      def __init__(self,lat,lon):
            self.lat=lat
            self.lon=lon

class Eqs:
      def __init__(self,lat,lon,mag):
            self.lat=lat
            self.lon=lon
            self.mag=mag

#####
sta_list=[]
eq_list=[]

with open('All.stations', "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            sta_list.append(Stations(float(items[3]),float(items[4])))

with open('All.events', "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            eq_list.append(Eqs(float(items[5]),float(items[6]),float(items[3])))

######
boundaries = requests.get("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json").json()
# yes_plume = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/yes_plume_vertical_lat_long.txt'

fig, ax=plt.subplots(figsize=(9,6))
plt.axis('off')
plt.ion()
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=-70))
# ax = plt.axes(projection=ccrs.Robinson(central_longitude=sta_long))
# ax = plt.axes(projection=ccrs.AzimuthalEquidistant(central_longitude=sta_long,central_latitude=sta_lat))
ax.set_global()
# ax.stock_img()
ax.set_facecolor('none')
ax.add_feature(cfeature.OCEAN.with_scale('110m'), facecolor='gainsboro', zorder=0)
ax.add_feature(cfeature.LAND.with_scale('110m'), facecolor='white', edgecolor='black', linewidth=0.2, zorder=1)

ax.coastlines(color='black', linewidth=.55)

for sta in sta_list:
    ax.scatter(sta.lon,sta.lat,marker='v', s=12, transform=ccrs.Geodetic(),c='none',edgecolors='teal',alpha=.4,lw=.3)

for eq in eq_list:
    ax.scatter(eq.lon,eq.lat,marker='o', s=7, transform=ccrs.Geodetic(),c='brown',edgecolors='white',alpha=.75,lw=.15)

for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)

# ax.set_frame_on(False)
plt.show()

# plt.savefig('st_all.jpg',dpi=400,bbox_inches='tight', pad_inches=0,transparent=True)
