import numpy as np
import re
import argparse


def remove_nonnumeric(stri):
    # print(stri)
    return re.sub("[^\d.]", "",stri)

### Sees if string has a digit
def hasdigit(stri):
    return any(char.isdigit() for char in stri)

### finds the next number in list of objs @ i + 2, i + 3, i + 4
### need different i's because some city have space in their name
def find_number(i,objs):
    if hasdigit(objs[i+2]):
        return objs[i+2].replace(",","")
    elif hasdigit(objs[i+3]):
        return objs[i+3].replace(",","")
    elif hasdigit(objs[i+4]):
        return objs[i+4].replace(",","")
    elif hasdigit(objs[i+5]):
        return objs[i+5].replace(",","")
    return -1
### finds how many males and how many felames after the word vs
def find_vs_number(i,objs):
    if hasdigit(objs[i+2]):
        return objs[i+2].replace(",",""),objs[i+4].replace(",","")
    elif hasdigit(objs[i+3]):
        return objs[i+3].replace(",",""),objs[i+5].replace(",","")
    return objs[i+4].replace(",",""),objs[i+6].replace(",","")
### finds the ages after the word age for male and females
def find_ages_number(i,objs):
    if hasdigit(objs[i+2]):
        return objs[i+2].replace(",",""),objs[i+5].replace(",","")
    elif hasdigit(objs[i+3]):
        return objs[i+3].replace(",",""),objs[i+6].replace(",","")
    return objs[i+4].replace(",",""),objs[i+6].replace(",","")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_location', help='The path to the file containing the text data copied from city-data.com')
    args = parser.parse_args()
    ### Read in the data  Data copied from city-data.com for provo neighboorhoods
    with open(args.data_location) as f:
        objs = f.readline().split(" ")

    ### The Different Fields ###
    areas = []
    population_density = []
    income = []
    rent = []
    males = []
    females = []
    males_age = []
    females_age = []

    for i,obj in enumerate(objs):
        if obj == "Area:":
            areas += [find_number(i,objs)]
        if obj == "density:":
            population_density += [find_number(i,objs)]
        if obj == "income":
            income += [find_number(i+1,objs)]
        if obj == "rent":
            rent += [find_number(i+2,objs)]
        if obj == "vs":
            m,f = find_vs_number(i,objs)
            males += [m]
            females += [f]
        if obj == "age":
            m,f = find_ages_number(i,objs)
            males_age += [m]
            females_age += [f]

    data = np.vstack([population_density,income,rent,males,females,males_age,females_age])
    datashape = data.shape
    ## Cleaning the Data
    ndata = np.array([remove_nonnumeric(d) for d in data.flatten()])
    ndata = ndata.reshape(datashape)
    ndata = ndata.astype(float)\
    ## Saving the Data
    np.savetxt("provo_city_data/DataFormated.csv",ndata.T,delimiter=",",fmt='%.2f')


if __name__ == "__main__":
    main()
