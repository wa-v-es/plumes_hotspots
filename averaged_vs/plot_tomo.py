import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
# Load tomography data, skip first 3 lines
tomo_file = 'SubMachine_depth_slice_2850.txt'
data = np.loadtxt(tomo_file, skiprows=3)
lons, lats, values = data[:, 0], data[:, 1], data[:, 2]

lons = (lons + 180) % 360 - 180

proj = ccrs.Mollweide(central_longitude=100)
fig, ax = plt.subplots(subplot_kw={'projection': proj}, figsize=(12, 6))

sc = ax.scatter(lons, lats, c=values, cmap='RdBu', vmin=-1, vmax=1,
                transform=ccrs.PlateCarree(), s=10)

cbar = plt.colorbar(sc, orientation='horizontal', pad=0.02, shrink=0.4)
cbar.set_label('Normalised dVs/Vs %')
ax.coastlines(linewidth=0.7)
# ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# plume vertical (columns 3 = lat, 4 = lon)
plume_file = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/plume_vertical_lat_long.txt'
plume_data = np.genfromtxt(plume_file)
plume_lats = plume_data[:, 1]
plume_lons = plume_data[:, 2]

plume_lons = (plume_lons + 180) % 360 - 180

ax.scatter(plume_lons, plume_lats, marker='D', color='black', s=30,
           transform=ccrs.PlateCarree(), label='Hotspots')

ax.legend(loc='lower left')

# plt.title('Tomography Map with Plume Locations')
plt.tight_layout()
# plt.show()
plt.savefig('5vs_avg_2850.png', dpi=350, bbox_inches='tight', pad_inches=0.1)
