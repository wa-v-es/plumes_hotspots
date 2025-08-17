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
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


class Stations:
      def __init__(self,lat,lon,num):
            self.lat=lat
            self.lon=lon
            self.number=num

class Eqs:
      def __init__(self,lat,lon,mag):
            self.lat=lat
            self.lon=lon
            self.mag=mag

#####

def get_plume_latlong(plume_file):
    plume_data = np.genfromtxt(plume_file)
    plume_lats = plume_data[:, 1]
    plume_lons = plume_data[:, 2]
    plume_lons = (plume_lons + 180) % 360 - 180

    return plume_lons, plume_lats


boundaries = requests.get("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json").json()
yes_plume = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/yes_plume_vertical_lat_long.txt'
plume_lons, plume_lats = get_plume_latlong(yes_plume)

sta_list=[]
with open('/Users/keyser/Research/plumes_hotspots/otter/heatmap_out/arrSta_rad2.5.txt', "r") as infile:
        # headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            sta_list.append(Stations(float(items[4]),float(items[5]),float(items[0])))
#
sta_list2=[]
with open('/Users/keyser/Research/plumes_hotspots/otter/heatmap_out/arrSta_eq2_1.5.txt', "r") as infile:
        # headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            sta_list2.append(Stations(float(items[4]),float(items[5]),float(items[0])))

sta_list3=[]
with open('/Users/keyser/Research/plumes_hotspots/otter/heatmap_out/arrSta_eq3_1.5.txt', "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            sta_list3.append(Stations(float(items[4]),float(items[5]),float(items[0])))

##
proj = ccrs.Stereographic(central_longitude=10, central_latitude=90, true_scale_latitude=60)
# proj = ccrs.TransverseMercator(10)
# plt.clf()
plt.ion()
fig = plt.figure(figsize=(15, 8), facecolor=None)
ax1 = plt.subplot(1, 1, 1, projection=proj)
ax1.set_extent([-11, 37, 35, 60], crs=ccrs.PlateCarree())
# ax = plt.axes(ccrs.Stereographic(central_longitude=10, central_latitude=90, true_scale_latitude=60))
ax1.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor='xkcd:dusty blue', zorder=0,alpha=.4)
ax1.add_feature(cfeature.LAND.with_scale("50m"), facecolor="white", zorder=1)

# Add coastlines on top
ax1.coastlines(resolution="50m", color="black", linewidth=0.5, zorder=99)

gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=.8, color='gray', alpha=0.5, linestyle='--',rotate_labels=False,
        x_inline=False, y_inline=False)

gl.xlocator = mticker.FixedLocator([-10,0,10,20,30,40])
gl.ylocator = mticker.FixedLocator([35,45,55])

# gl.xlines = True
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 14}
gl.ylabel_style = {'size': 14}
###
list=[120,121,122,123]
for sta in sta_list:
    ax1.scatter(sta.lon,sta.lat,marker='v', s=30, transform=ccrs.Geodetic(),c='none',edgecolors='teal',lw=.8)
    # if int(sta.number) in list:
    #     ax1.scatter(sta.lon,sta.lat,marker='v', s=50, transform=ccrs.Geodetic(),c='maroon',edgecolors='maroon',lw=.6)

#
# for sta in sta_list2:
#     ax1.scatter(sta.lon,sta.lat,marker='o', s=12, transform=ccrs.Geodetic(),c='none',edgecolors='maroon',lw=.4)
plt.savefig('europe_sts.jpg',dpi=400,bbox_inches='tight', pad_inches=0,transparent=True)
