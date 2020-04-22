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
    # print(df)
    # continue
    for _, n in tqdm(df.iterrows(), total=df.shape[0]):
        # print(n)
        if n['Type'] != 'WIFI':
            continue
        if n['CurrentLongitude'] > -100:
            continue # Ignore Ohio results
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

# https://stackoverflow.com/questions/2369492/generate-a-heatmap-in-matplotlib-using-a-scatter-data-set

ranges = [[min(lons['WEP']+lons['OTHER']),max(lons['WEP']+lons['OTHER'])],
            [min(lats['WEP']+lats['OTHER']),max(lats['WEP']+lats['OTHER'])]]


heatmap1, xedges1, yedges1 = np.histogram2d(lons['WEP'],lats['WEP'],range=ranges,bins=75)
heatmap2, xedges1, yedges1 = np.histogram2d(lons['OTHER'],lats['OTHER'],range=ranges,bins=75)

heatmap3 = heatmap1 + heatmap2
heatmap4 = np.divide(heatmap1, heatmap3, out=np.zeros_like(heatmap1), where=heatmap3!=0)
## HeatMap4 is the percentage of WEP out of Total Networks ##

extent = [xedges1[0], xedges1[-1], yedges1[0], yedges1[-1]]
fig,ax = plt.subplots(1,1)

## I don't have the actual image so this will do for now LOL.
mp = plt.imread('graphics/utah.png')
im1 = plt.imshow(mp,extent=extent)
ax.set_title('Heatmap WEP usage in Provo')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')


ax.imshow(heatmap4.T,cmap= plt.cm.hot,extent=extent,alpha=.5,origin='lower')

plt.savefig("graphics/UtahApril17HeatMap.png")
