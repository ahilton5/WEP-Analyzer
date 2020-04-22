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

ssids = [networks[n]['SSID'] for n in networks]

wep_ssids = [networks[n]['SSID'] for n in weps]

c = Counter(ssids)
print('Most Common SSIDs')
for name, count in c.most_common(10):
    print(name, count, f'{count*100/len(ssids):0.2f}%', sep='\t')

c = Counter(wep_ssids)
print('Most SSIDs with WEP')
for name, count in c.most_common():
    print(name, f'{count*100/len(wep_ssids):0.2f}%', sep=' & ')

