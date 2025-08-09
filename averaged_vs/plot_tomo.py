import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
from scipy.interpolate import griddata
# Load tomography data, skip first 3 lines

def get_plume_latlong(plume_file):
    plume_data = np.genfromtxt(plume_file)
    plume_lats = plume_data[:, 1]
    plume_lons = plume_data[:, 2]
    plume_lons = (plume_lons + 180) % 360 - 180

    return plume_lons, plume_lats

plt.rcParams['font.size'] = 13
tomo_file = 'SubMachine_depth_slice_2850.txt'
data = np.loadtxt(tomo_file, skiprows=3)
lons, lats, values = data[:, 0], data[:, 1], data[:, 2]

lons = (lons + 180) % 360 - 180
# grid data for making contour
lon_grid = np.linspace(lons.min(), lons.max(), 200)
lat_grid = np.linspace(lats.min(), lats.max(), 200)
lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

# Interpolate to the grid
grid_values = griddata(
    points=(lons, lats),
    values=values,
    xi=(lon_mesh, lat_mesh),
    method='linear'
)

proj = ccrs.Mollweide(central_longitude=100)
fig, ax = plt.subplots(subplot_kw={'projection': proj}, figsize=(12, 6))

sc = ax.scatter(lons, lats, c=values, cmap='RdBu', vmin=-1, vmax=1,
                transform=ccrs.PlateCarree(), s=10)
contour = ax.contour(
    lon_mesh, lat_mesh, grid_values,
    levels=[-0.15],
    colors='maroon',
    linewidths=1.5,
    transform=ccrs.PlateCarree()
)

cbar = plt.colorbar(sc, orientation='horizontal', pad=0.02, shrink=0.4)
cbar.set_label('Normalised dVs/Vs %')
ax.coastlines(linewidth=0.7)
# ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# plume vertical (columns 3 = lat, 4 = lon)
all_plume_file = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/all_plume_vertical_lat_long.txt'
yes_plume = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/yes_plume_vertical_lat_long.txt'
no_plume = '/Users/keyser/Research/plumes_hotspots/jackson_etal_2021/no_plume_vertical_lat_long.txt'

plume_lons, plume_lats = get_plume_latlong(yes_plume)
no_plume_lons, no_plume_lats = get_plume_latlong(no_plume)



ax.scatter(plume_lons, plume_lats, marker='D', color='black', s=45,
           transform=ccrs.PlateCarree(), label='Plume detected')
ax.scatter(no_plume_lons, no_plume_lats, marker='D', color='whitesmoke', edgecolors='black', s=45,
           transform=ccrs.PlateCarree(), label='No plume detected')

ax.legend(loc='lower left')

# plt.title('Tomography Map with Plume Locations')
plt.tight_layout()
# plt.show()
plt.savefig('5vs_avg_2850_cont.png', dpi=350, bbox_inches='tight', pad_inches=0.1)
