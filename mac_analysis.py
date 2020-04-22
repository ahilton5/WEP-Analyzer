from os.path import isfile, join
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from os import listdir
from tqdm import tqdm
import pandas as pd
import numpy as np
import argparse
import random
import json

parser = argparse.ArgumentParser()
parser.add_argument('data_location', help='The directory containing all the csv files output by WiGLE.')
parser.add_argument('mal', help='List of vendor MA-L prefixes, downloaded from https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries')
parser.add_argument('mam', help='List of vendor MA-M prefixes, downloaded from https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries')
parser.add_argument('mas', help='List of vendor MA-S prefixes, downloaded from https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries')
args = parser.parse_args()

networks = {}
weps = {}

for fname in [join(args.data_location, f) for f in listdir(args.data_location) if isfile(join(args.data_location, f))]:
    print(f'Processing {fname}...')
    df = pd.read_csv(fname, encoding = "ISO-8859-1")
    for _, n in tqdm(df.iterrows(), total=df.shape[0]):
        if n['Type'] != 'WIFI':
            continue
        networks[n['MAC']+ str(n['SSID'])] = {'AuthMode': n['AuthMode'], 'CurrentLatitude': n['CurrentLatitude'], 'CurrentLongitude': n['CurrentLongitude'], 'SSID': n['SSID'], 'MAC': n['MAC']}
        if isinstance(n['AuthMode'], str) and 'WEP' in n['AuthMode']:
            weps[n['MAC']+ str(n['SSID'])] = n

macToVendor = defaultdict(lambda: 'Unknown')
mal = defaultdict(lambda: 'Unknown')
print(f'Loading {args.mal}...')
df = pd.read_csv(args.mal)
prefixes = df['Assignment'].tolist()
vendors = df['Organization Name'].tolist()
for prefix, vendor in zip(prefixes, vendors):
    mal[prefix] = vendor

mam = defaultdict(lambda: 'Unknown')
print(f'Loading {args.mam}...')
df = pd.read_csv(args.mam)
prefixes = df['Assignment'].tolist()
vendors = df['Organization Name'].tolist()
for prefix, vendor in zip(prefixes, vendors):
    mam[prefix] = vendor

mas = defaultdict(lambda: 'Unknown')
print(f'Loading {args.mas}...')
df = pd.read_csv(args.mas)
prefixes = df['Assignment'].tolist()
vendors = df['Organization Name'].tolist()
for prefix, vendor in zip(prefixes, vendors):
    mas[prefix] = vendor

def getVendor(mac):
    mac = mac.replace(':','').upper()
    if mal[mac[:6]] not in ['Unknown', 'IEEE Registration Authority']:
        return mal[mac[:6]]
    elif mam[mac[:7]] not in ['Unknown', 'IEEE Registration Authority']:
        return mam[mac[:7]]
    else:
        return mas[mac[:9]]

macs = [networks[n]['MAC'] for n in networks]
vendors = [getVendor(mac) for mac in tqdm(set(macs))]

wep_macs = [networks[n]['MAC'] for n in weps]
wep_vendors = [getVendor(mac) for mac in tqdm(set(wep_macs))]

c = Counter(vendors)
print('Most Common Vendors')
for name, count in c.most_common(10):
    print(name, count, f'{count*100/len(vendors):0.2f}%', sep='\t')

c = Counter(wep_vendors)
print('Most Common Vendors with WEP')
for name, count in c.most_common():
    print(name, f'{count*100/len(wep_vendors):0.2f}%', sep=' & ')

