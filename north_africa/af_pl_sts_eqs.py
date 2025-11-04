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
from obspy.taup import TauPyModel
import pyproj

from obspy.taup.taup_geo import calc_dist,calc_dist_azi
sys.path.append("/Users/keyser/Research/plumes_hotspots/carribean")

import circle as cir_robin


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
ta_list=[]
eq_list=[]
se_asia_eq_list=[]

# three af plumes_ lat long_ (jackson et al 2021, French & Roma: plume yes or no)
haggar_ll=(23.2,	5.7)#(yes, no)
darfur_ll=(13.0,	24.3)# (no, yes)
tibesti_ll=(19.9,	18.6)# (no, no)

# sys.exit()
st_all='/Users/keyser/Research/plumes_hotspots/otter/All.stations'
eq_all='/Users/keyser/Research/plumes_hotspots/otter/All.events'

with open(st_all, "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            sta_list.append(Stations(float(items[3]),float(items[4])))
            if 25 < float(items[3]) < 50 and -125 < float(items[4])< -65:
                ta_list.append(Stations(float(items[3]),float(items[4])))

with open(eq_all, "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            year=UTCDateTime(items[1]).year
            eq_list.append(Eqs(float(items[5]),float(items[6]),float(items[3])))
            if float(items[5]) < 10 and 2004 < year < 2015:
                if 90 < float(items[6]) or -168 > float(items[6]):

                    se_asia_eq_list.append(Eqs(float(items[5]),float(items[6]),float(items[3])))

print('# eqs:',len(se_asia_eq_list))
######
global_ = False
TA_only = True
boundaries = requests.get("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json").json()
# yes_plume = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/yes_plume_vertical_lat_long.txt'
geod=pyproj.Geod(ellps="WGS84")

fig, ax=plt.subplots(figsize=(15,10))
plt.axis('off')
plt.ion()
ax = plt.axes(projection=ccrs.Robinson())# Stereographic was mollewide
# ax = plt.axes(projection=ccrs.Robinson(central_longitude=20))#  was mollewide

# ax = plt.axes(projection=ccrs.Robinson(central_longitude=sta_long))
# ax = plt.axes(projection=ccrs.AzimuthalEquidistant(central_longitude=sta_long,central_latitude=sta_lat))
ax.set_global()
# ax.stock_img()
ax.set_facecolor('none')
ax.add_feature(cfeature.OCEAN.with_scale('110m'), facecolor='gainsboro', zorder=0)
ax.add_feature(cfeature.LAND.with_scale('110m'), facecolor='white', edgecolor='black', linewidth=0.2, zorder=1)

ax.coastlines(color='black', linewidth=.55)

X,Y=cir_robin.equi(tibesti_ll[1], tibesti_ll[0], 7700)
X1,Y1=cir_robin.equi(tibesti_ll[1], tibesti_ll[0], 19800)

plt.plot(X,Y,transform=ccrs.Geodetic(),lw=2,alpha=1,linestyle='--',c='royalblue')
plt.plot(X1,Y1,transform=ccrs.Geodetic(),lw=2,alpha=1,linestyle='--',c='royalblue')
ax.text(20, -55, '70°',fontsize=14,fontfamily='serif', color='royalblue',transform=ccrs.Geodetic())
ax.text(140, 25, 'Eqs ({}) 2004-15'.format(len(se_asia_eq_list)),fontsize=11,fontfamily='serif', color='black',transform=ccrs.Geodetic())

if global_:
    for sta in sta_list:
        ax.scatter(sta.lon,sta.lat,marker='v', s=12, transform=ccrs.Geodetic(),c='none',edgecolors='teal',alpha=.4,lw=.3)
    for eq in eq_list:
        ax.scatter(eq.lon,eq.lat,marker='o', s=7, transform=ccrs.Geodetic(),c='brown',edgecolors='white',alpha=.75,lw=.15)

if TA_only:
    for sta in ta_list:
        ax.scatter(sta.lon,sta.lat,marker='v', s=12, transform=ccrs.Geodetic(),c='none',edgecolors='teal',alpha=.4,lw=.3)
    for eq in se_asia_eq_list:
        ax.scatter(eq.lon,eq.lat,marker='o', s=7, transform=ccrs.Geodetic(),c='brown',edgecolors='white',alpha=.75,lw=.15)

for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)

# US edges LAT 25, 50..LONG -65, -125


for eq in se_asia_eq_list:
    # line_arc=geod.inv_intermediate(eq.lon,eq.lat,-65,25,npts=300)
    # lon_points=np.array(line_arc.lons)
    # lat_points=np.array(line_arc.lats)
    # plt.plot(lon_points, lat_points, transform=ccrs.Geodetic(),color='darkgreen',lw=.05,alpha=.1)
    plt.plot([-65,eq.lon],[25, eq.lat],  transform=ccrs.Geodetic(),color='darkgreen',lw=.09,alpha=.15)#,linestyle='dotted'
    # plt.plot([-125,eq.lon],[25, eq.lat],  transform=ccrs.Geodetic(),color='darkgreen',lw=.05,alpha=.1)#,linestyle='dotted'
    # plt.plot([-65,eq.lon],[50, eq.lat],  transform=ccrs.Geodetic(),color='darkgreen',lw=.05,alpha=.1)#,linestyle='dotted'
    # plt.plot([-125,eq.lon],[50, eq.lat],  transform=ccrs.Geodetic(),color='darkgreen',lw=.05,alpha=.1)#,linestyle='dotted'


ax.scatter(haggar_ll[1], haggar_ll[0], marker='D', color='gold', s=55,
           transform=ccrs.PlateCarree())
ax.scatter(darfur_ll[1], darfur_ll[0], marker='D', color='gold', s=55,
           transform=ccrs.PlateCarree())
ax.scatter(tibesti_ll[1], tibesti_ll[0], marker='D', color='gold', s=55,
           transform=ccrs.PlateCarree())
# ax.set_frame_on(False)



plt.show()

# plt.savefig('af_st_eq_all.jpg',dpi=400,bbox_inches='tight', pad_inches=0,transparent=True)
