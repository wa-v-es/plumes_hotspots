#purpose is to calculate how many arrays for an earthquake from a heatmap.json file
import jsonpickle
import os
# from heatmap import Gridpoint,Station,EQ,Location
# from heatmap import EqtoArrayList
from types import SimpleNamespace

infilename = "heatmap.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())

mydata = SimpleNamespace(mydata)

good_arrays=mydata.good_arrays
eq_list=mydata.eq_list
minsta=mydata.minsta

eqtoarr=[]

for evt in eq_list:
    eqtoarr.append(EqtoArrayList(evt))

phaseToDist = {'P': (30, 90)}
print(f'there are {len(eqtoarr)} eq in catalog')

for evt in eqtoarr:
    for phase, dist in phaseToDist.items():
        arr_count=0
        for arr in good_arrays:
            evt.check_array(arr,dist,minsta)

over_200=0
over_100=0
for evt in eqtoarr:
    if len(evt.array_list)> 100:
        over_100+=1
    if len(evt.array_list)> 200:
        over_200+=1
print(f'there are {over_200} earthquakes that can form more than 200 arrays')
print(f'there are {over_100} earthquakes that can form more than 100 arrays')
