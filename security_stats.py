from os.path import isfile, join
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from os import listdir
from tqdm import tqdm
import pandas as pd
import numpy as np
import argparse
import random
import json

def printCounts(security_type):
    counts = Counter(security_type)
    total = np.sum([c for c in counts.values()])
    for name,c in counts.items():
        print(name,c,c/total) 


def sortBySecurity(networks):
    security_type = []
    for authmode in networks.values():
        if "WPA" in authmode:
            security_type += ["WPA"]
        elif "WEP" in authmode:
            security_type += ["WEP"]
        elif "IBSS" in authmode:
            security_type += ["IBSS"]
        elif "RSN" in authmode:
            security_type += ["RSN"]
        elif "ESS" in authmode:
            security_type += ["OPEN"]
        else:
            security_type += ["OTHER"]
    return security_type



parser = argparse.ArgumentParser()
parser.add_argument('data_location', help='The directory containing all the csv files output by WiGLE.')
# parser.add_argument('-j', help='Add random jitter to the points on the map to spread the data out and add anonymity.', action='store_true')
args = parser.parse_args()

networks_utah = {}
networks_ohio = {}
for fname in [join(args.data_location, f) for f in listdir(args.data_location) if isfile(join(args.data_location, f))]:
    print(f'Processing {fname}...')
    df = pd.read_csv(fname, encoding = "ISO-8859-1")
    for _, n in tqdm(df.iterrows(), total=df.shape[0]):
        # print(n)
        if n['Type'] != 'WIFI':
            continue
        if n['CurrentLongitude'] > -100:
            networks_ohio[n['MAC']+ str(n['SSID'])] = str(n['AuthMode'])
        else:
            networks_utah[n['MAC']+ str(n['SSID'])] = str(n['AuthMode'])




security_utah = sortBySecurity(networks_utah)
security_ohio = sortBySecurity(networks_ohio)

print("security_utah\n")
printCounts(security_utah)


print("\nsecurity_ohio\n")
printCounts(security_ohio)


