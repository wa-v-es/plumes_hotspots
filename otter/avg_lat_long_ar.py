from collections import defaultdict
import numpy as np
import os
import sys
from obspy.taup.taup_geo import calc_dist,calc_dist_azi
from obspy.taup import TauPyModel


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
print("ID\tAvg_Lat\t\tAvg_Long")
for key in sorted(count.keys(), key=int):
    avg_lat = sum_lat[key] / count[key]
    avg_long = sum_long[key] / count[key]

    dist=calc_dist(eq_lat,eq_long,avg_lat,avg_long,6400,0)
    dist_all.append(dist)

dist_all=np.array(dist_all)
print(f"Min dist: {np.min(dist_all):.2f}\t; Max dist:{np.max(dist_all):.2f}")
