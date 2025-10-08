from collections import defaultdict
import numpy as np
import os
import sys
from obspy.taup.taup_geo import calc_dist,calc_dist_azi
from obspy.taup import TauPyModel
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

# File path
file_path = "heatmap_out/arrSta_eq2_2.5.txt"

# Dictionary
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

model = TauPyModel(model="ak135")
dist_all=[]
# print("ID\tAvg_Lat\t\tAvg_Long")
for key in sorted(count.keys(), key=int):
    avg_lat = sum_lat[key] / count[key]
    avg_long = sum_long[key] / count[key]

    dist=calc_dist(eq_lat,eq_long,avg_lat,avg_long,6400,0)
    dist_all.append(dist)

dist_all=np.array(dist_all)
print(f"Min dist: {np.min(dist_all):.2f}\t; Max dist:{np.max(dist_all):.2f}")
#

rect_top=1000.0
rect_bottom=2890.0
rect_width=600.0
circle_radius=500.0
circle_center_depth=500
x_lim=1000
y_lim_top=0
y_lim_bottom=2900
outpath="plume_fig.png"
dpi=300

# Rectangle coords
rect_half = rect_width / 2.0
rect_x = -rect_half
rect_y = rect_top
rect_height = rect_bottom - rect_top
plt.style.use('ggplot')
plt.rcParams['font.size'] = 15

fig, ax = plt.subplots(figsize=(8, 8))
rect = Rectangle((rect_x, rect_y), rect_width, rect_height,facecolor='khaki',edgecolor='grey',linewidth=.1,alpha=.55)
ax.add_patch(rect)

circle = Circle((0.0, circle_center_depth), circle_radius,facecolor='darkkhaki',edgecolor='grey',linewidth=.1,alpha=.55)
ax.add_patch(circle)

ax.set_xlim(-1200, 1200)
ax.set_ylim(y_lim_top, y_lim_bottom)
ax.invert_yaxis()

ax.vlines(-200, 1250, 2700, colors='navy', linewidth=2)
ax.text(-200, (1250+2700)/2, 'P', ha='center', va='center',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
ax.vlines(-100, 700, 1100, colors='navy', linewidth=2)
ax.text(-100, (700+1100)/2, 'PP', ha='center', va='center',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
ax.vlines(100, 1200, 2600, colors='palevioletred', linewidth=2)
ax.text(100, (1200+2600)/2, 'S', ha='center', va='center',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
ax.vlines(200, 600, 1100, colors='palevioletred', linewidth=2)
ax.text(200, (600+1100)/2, 'SS', ha='center', va='center',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
ax.vlines(300, 1400, 1800, colors='palevioletred', linewidth=2)
ax.text(300, (1400+1900)/2, 'PS', ha='center', va='center',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))


ax.set_xlabel("")
ax.set_xticks([])
ax.set_ylabel("Depth (km)")

# ax.set_xticks([-x_lim, -x_lim//2, 0, x_lim//2, x_lim])

# ax.set_title("Plume (rectangle) with overlying circle (centered at lon 0)")

# ax.text(20, rect_top + 150, f"Rectangle: {int(rect_top)}–{int(rect_bottom)} km depth, width {int(rect_width)} km", va="top")
# ax.text(20, circle_center_depth - 250, f"Circle: radius {int(circle_radius)} km, center at depth {int(circle_center_depth)} km", va="top")

plt.tight_layout()
# plt.show()
fig.savefig(outpath, dpi=dpi,bbox_inches='tight', pad_inches=0.1)
# plt.close(fig)
