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


import circle as cir_robin
from importlib import reload
reload(cir_robin)
import requests
from obspy.taup.taup_geo import calc_dist,calc_dist_azi
def get_plume_latlong(plume_file):
    plume_data = np.genfromtxt(plume_file)
    plume_lats = plume_data[:, 1]
    plume_lons = plume_data[:, 2]
    plume_lons = (plume_lons + 180) % 360 - 180

    return plume_lons, plume_lats


boundaries = requests.get("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json").json()
yes_plume = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/yes_plume_vertical_lat_long.txt'
plume_lons, plume_lats = get_plume_latlong(yes_plume)

####
station='ILAR'
sta_lat= -2
sta_long=-70

eur_lat= 45
eur_long= 10

client = Client("IRIS")

# eq_map = Basemap(projection='robin', resolution = 'i', area_thresh = 1000.0,
#               lat_0=sta_lat, lon_0=sta_long)
# eq_map.drawcoastlines()
# eq_map.drawcountries()
# eq_map.fillcontinents(color = 'LightGoldenrodYellow')
# eq_map.drawmapboundary()
# eq_map.drawmeridians(np.arange(0, 360, 60))
# eq_map.drawparallels(np.arange(-90, 90, 30))
# plt.show()

###########
# catfile = 'events_ak_2024_6.7.xml'
# catfile = 'events_ZS_2019_6.7.xml'
catfile_NW = 'events_6.xml'

### get eq data
#earthquakes
starttime= UTCDateTime('1994-01-01T00:00:01')
endtime= UTCDateTime('2025-08-01T00:00:01')

# starttime= UTCDateTime('2017-10-01T00:00:01') # for ZS
# endtime= UTCDateTime('2019-12-31T00:00:01') # for ZS

if not os.path.exists(catfile_NW):
    catalog = client.get_events(starttime=starttime, endtime=endtime,minmagnitude=6,\
    latitude=sta_lat,longitude=sta_long, minradius=1, maxradius=30,mindepth=1)
    catalog.write(catfile_NW, 'QUAKEML')

catalog_NW=read_events(catfile_NW)
# catalog_NW.plot()
lats, longs = [], []
mags = []
azi=[]
dists=[]
#
for event in catalog_NW:
    lats.append(event.origins[0].latitude)
    longs.append(event.origins[0].longitude)
    mags.append(event.magnitudes[0].mag)
    dist=calc_dist(event.origins[0].latitude,event.origins[0].longitude,sta_lat,sta_long,6400,0)
    dists.append(dist)

print('{} event in catalog'.format(len(catalog_NW)))
#
###
fig, ax=plt.subplots(figsize=(9,6))
plt.axis('off')

ax = plt.axes(projection=ccrs.Mollweide(central_longitude=-20))
# ax = plt.axes(projection=ccrs.Robinson(central_longitude=sta_long))
# ax = plt.axes(projection=ccrs.AzimuthalEquidistant(central_longitude=sta_long,central_latitude=sta_lat))
ax.set_global()
# ax.stock_img()
ax.set_facecolor('none')
ax.add_feature(cfeature.OCEAN.with_scale('110m'), facecolor='xkcd:dusty blue', zorder=0,alpha=.4)
ax.add_feature(cfeature.LAND.with_scale('110m'), facecolor='white', edgecolor='black', linewidth=0.2, zorder=1)

ax.coastlines(color='black', linewidth=.55)
# ax.plot(sta_long, sta_lat, color='indigo', marker='^', markersize=7, transform=ccrs.Geodetic())
# ax.plot(sta_long_, sta_lat_, color='indigo', marker='^', markersize=7, transform=ccrs.Geodetic())

min_marker_size = .35
for i in range(len(lats)): #plot eqs
    # x,y = eq_map(lon, lat)
    msize = mags[i] * min_marker_size
    # marker_string = get_marker_color(mag)
    ax.plot(longs[i], lats[i],color='darkgreen',marker='o',markersize=msize,alpha=.4,transform=ccrs.Geodetic())


X,Y=cir_robin.equi(sta_long, sta_lat, 3300)
X1,Y1=cir_robin.equi(sta_long, sta_lat, 9900)

plt.plot(X,Y,transform=ccrs.Geodetic(),lw=.9,alpha=.6,linestyle='--',c='maroon')
plt.plot(X1,Y1,transform=ccrs.Geodetic(),lw=.9,alpha=.6,linestyle='--',c='maroon')

ax.scatter(plume_lons, plume_lats, marker='D', color='black', s=25,
           transform=ccrs.PlateCarree(), label='Plume detected')
#plot gcp
for event in catalog_NW:
    ori= event.preferred_origin()
    plt.plot([eur_long,ori.longitude ],[eur_lat, ori.latitude],  transform=ccrs.Geodetic(),color='darkgreen',lw=.1,alpha=.15)#,linestyle='dotted'

# Plot boundaries.
# for f in boundaries["features"]:
#     c = np.array(f["geometry"]["coordinates"])
#     lng, lat = c[:, 0], c[:, 1]
#     x, y = lng, lat
#     mask = np.bitwise_or(np.abs(x) > 1e15, np.abs(y) > 1e15)
#     x = np.ma.array(x)
#     y = np.ma.array(y)
#     x.mask = mask
#     y.mask = mask
#     plt.plot(x, y, color="Navy", lw=.35,transform=ccrs.Geodetic())

# ax.text(sta_long+5, sta_lat-3, 'AK',fontsize=8,fontfamily='serif', color='indigo',transform=ccrs.Geodetic())
# ax.text(sta_long_+5, sta_lat_-3, 'AK_SE',fontsize=8,fontfamily='serif', color='indigo',transform=ccrs.Geodetic())

# ax.text(-145, -8, '65°',fontsize=10,fontfamily='serif', color='maroon',transform=ccrs.Geodetic())
# ax.text(-145, -42, '100°',fontsize=10,fontfamily='serif', color='maroon',transform=ccrs.Geodetic())
# ax.axis('off')
# ax.set_axis_off()
# ax.set_frame_on(False)

for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)

plt.show()

# sys.exit()
# plt.savefig('eq_6_molly_eu.jpg',dpi=400,bbox_inches='tight', pad_inches=0,transparent=True)
###
