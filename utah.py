from os.path import isfile, join
import matplotlib.pyplot as plt
from os import listdir
from tqdm import tqdm
import pandas as pd
import numpy as np
import argparse
import random
import json

parser = argparse.ArgumentParser()
parser.add_argument('data_location', help='The directory containing all the csv files output by WiGLE.')
parser.add_argument('-j', help='Add random jitter to the points on the map to spread the data out and add anonymity.', action='store_true')
args = parser.parse_args()

networks = {}
weps = {}

for fname in [join(args.data_location, f) for f in listdir(args.data_location) if isfile(join(args.data_location, f))]:
    print(f'Processing {fname}...')
    df = pd.read_csv(fname, encoding = "ISO-8859-1")
    for _, n in tqdm(df.iterrows(), total=df.shape[0]):
        if n['Type'] != 'WIFI':
            continue
        if n['CurrentLongitude'] > -100:
            continue # Ignore Utah results
        networks[n['MAC']+ str(n['SSID'])] = {'AuthMode': n['AuthMode'], 'CurrentLatitude': n['CurrentLatitude'], 'CurrentLongitude': n['CurrentLongitude']}
        if isinstance(n['AuthMode'], str) and 'WEP' in n['AuthMode']:
            weps[n['MAC']+ str(n['SSID'])] = n

print('Preparing map...')
lats = {'WEP': [], 'OTHER': []}
lons = {'WEP': [], 'OTHER': []}
for n in tqdm(networks):
    if isinstance(networks[n]['AuthMode'], str) and 'WEP' in networks[n]['AuthMode']:
        lats['WEP'].append(networks[n]['CurrentLatitude'])
        lons['WEP'].append(networks[n]['CurrentLongitude'])
    else:
        lats['OTHER'].append(networks[n]['CurrentLatitude'])
        lons['OTHER'].append(networks[n]['CurrentLongitude'])

BBox = ((min(lons['WEP']+lons['OTHER']), max(lons['WEP']+lons['OTHER']), min(lats['WEP']+lats['OTHER']), max(lats['WEP']+lats['OTHER'])))

print(BBox)
# https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db

print(f"{len(networks):,} networks found.")
print(f"{len(weps):,} use WEP ({len(weps)*100/len(networks):.2f}%).")

def spread(l):
    if not args.j:
        return l
    jitter = [random.random()/500 for _ in range(len(l))]
    for i in range(len(jitter)):
        if random.choice([True, False]):
            jitter[i]*=-1 
    return [jitter[i] + l[i] for i in range(len(l))]

mp = plt.imread('graphics/utah.png')
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(spread(lons['OTHER']), spread(lats['OTHER']), zorder=1, alpha= 0.1, c='steelblue', s=20)
ax.scatter(spread(lons['WEP']), spread(lats['WEP']), zorder=1, edgecolors='k', c='r', s=20)
ax.set_title('WEP Usage in Provo and Orem')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(mp, zorder=0, extent = BBox, aspect= 'equal')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.show()
