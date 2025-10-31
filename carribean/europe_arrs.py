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
from collections import defaultdict

def haversine_distance_km(lat1, lon1, lat2, lon2):

    R = 6371.0  # Earth radius in km
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c
###
def remove_close_stations(lat_arr, lon_arr, min_dist_km=100.0,method = "greedy"):

    lat = np.asarray(lat_arr).ravel()
    lon = np.asarray(lon_arr).ravel()
    if lat.shape != lon.shape:
        raise ValueError("lat_arr and lon_arr must have same shape.")
    n = lat.size
    if n == 0:
        return np.array([], dtype=int), np.zeros(0, dtype=bool)

    if method == "greedy":
        removed = np.zeros(n, dtype=bool)
        kept = []
        for i in range(n):
            if removed[i]:
                continue

            kept.append(i)

            dists = haversine_distance_km(lat[i], lon[i], lat, lon)

            close_mask = (dists < min_dist_km) & (np.arange(n) != i)
            removed[close_mask] = True
        keep_mask = np.zeros(n, dtype=bool)
        keep_mask[np.array(kept, dtype=int)] = True
        return np.array(kept, dtype=int), keep_mask

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

#
# Dictionary
file_path = "/Users/keyser/Research/plumes_hotspots/otter/heatmap_out/arrSta_eq2_1.5.txt"
sum_lat = defaultdict(float)
sum_long = defaultdict(float)
count = defaultdict(int)

eq_lat=20.0453
eq_long=-61.0681
with open(file_path, "r") as f:
    for line in f:
        parts = line.strip().split()
        key = parts[0]
        lat = float(parts[4])
        lon = float(parts[5])

        sum_lat[key] += lat
        sum_long[key] += lon
        count[key] += 1

lat_arr_all=[]
lon_arr_all=[]

# print("ID\tAvg_Lat\t\tAvg_Long")
for key in sorted(count.keys(), key=int):
    avg_lat = sum_lat[key] / count[key]
    avg_long = sum_long[key] / count[key]

    # dist=calc_dist(eq_lat,eq_long,avg_lat,avg_long,6400,0)
    # if count[key] > 15:
    lat_arr_all.append(avg_lat)
    lon_arr_all.append(avg_long)

lat_arr_all=np.array(lat_arr_all)
lon_arr_all=np.array(lon_arr_all)

print('Length of arrays:',len(lat_arr_all))
# sys.exit()

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
fig = plt.figure(figsize=(8, 8), facecolor=None)
ax1 = plt.subplot(1, 1, 1, projection=proj)
ax1.set_extent([-2, 42, 35, 53], crs=ccrs.PlateCarree())
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
for sta in sta_list2:
    ax1.scatter(sta.lon,sta.lat,marker='v', s=25, transform=ccrs.Geodetic(),c='none',edgecolors='teal',lw=.6)

kept_idx, mask=remove_close_stations(lat_arr_all,lon_arr_all,min_dist_km=200.0)
print('Length of arrays:',len(np.array(lon_arr_all)[kept_idx]))

# np.array(lat_arr)[kept_idx], np.array(lon_arr)[kept_idx]
# for i,lat in enumerate(lon_arr_all):
#     if i % 3 != 0:
#         ax1.scatter(lon_arr_all[i],lat_arr_all[i],marker='v', s=90, transform=ccrs.Geodetic(),c='darkred',edgecolors='white',lw=.8,alpha=.65)
ax1.scatter(np.array(lon_arr_all)[kept_idx],np.array(lat_arr_all)[kept_idx],marker='o', s=90, transform=ccrs.Geodetic(),c='darkred',edgecolors='white',lw=.8,alpha=.65)

    # if int(sta.number) in list:
    #     ax1.scatter(sta.lon,sta.lat,marker='v', s=50, transform=ccrs.Geodetic(),c='maroon',edgecolors='maroon',lw=.6)

#
# for sta in sta_list2:
#     ax1.scatter(sta.lon,sta.lat,marker='o', s=12, transform=ccrs.Geodetic(),c='none',edgecolors='maroon',lw=.4)
plt.show()
# plt.savefig('europe_sts.jpg',dpi=400,bbox_inches='tight', pad_inches=0,transparent=True)
