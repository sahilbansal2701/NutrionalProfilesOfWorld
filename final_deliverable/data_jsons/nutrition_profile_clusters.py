#!/usr/bin/env python

import sqlite3
import json
import pandas as pd
from sklearn.cluster import KMeans
from util import drop_incomplete_rows

database_path = "data/9-percentages/data.db"
MAX_CLUSTERS = 20

def uppercase_each_word(name):
    lst = name.split(' ')
    for i in range(len(lst)):
        if lst[i] == "and":
            continue
        if '-' in lst[i]:
            lst1 = name.split('-')
            for j in range(len(lst1)):
                lst1[j] = lst1[j].capitalize()
            lst[i] = '-'.join(lst1)
        else:
            lst[i] = lst[i].capitalize()
    return ' '.join(lst)


def main():  
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    years = dict()

    for year in range(2000, 2014, 1):
        print(year)
        countries = dict()
        c.execute("SELECT (CAST(fat_c AS FLOAT)/(meat_protein_c + plant_protein_c + carbohydrates_c + fat_c) * 100), (CAST(meat_protein_c + plant_protein_c AS FLOAT)/(meat_protein_c + plant_protein_c + carbohydrates_c + fat_c) * 100), (CAST(carbohydrates_c AS FLOAT)/(meat_protein_c + plant_protein_c + carbohydrates_c + fat_c) * 100), country FROM diet_and_life WHERE year = " + str(year))
        lst_tuples = c.fetchall()
        df = pd.DataFrame({
            "fat_p": [s[0] for s in lst_tuples],
            "protein_p": [s[1] for s in lst_tuples],
            "carbohydrates_p": [s[2] for s in lst_tuples],
            "country": [s[3] for s in lst_tuples],
        })
        df = drop_incomplete_rows(df)
        
        kmeans = KMeans(n_clusters=MAX_CLUSTERS, n_init='auto').fit(df[["fat_p", "protein_p", "carbohydrates_p"]])

        for j in range(MAX_CLUSTERS):
            mask = kmeans.labels_ == j
            list_countries_same_cluster = df["country"][mask].tolist()
            for country in list_countries_same_cluster:
                countries[country] = {"other_countries": [uppercase_each_word(i) for i in list_countries_same_cluster if i != country], 
                                      "fat_p": df.loc[df["country"] == country]["fat_p"].values[0],
                                      "protein_p": df.loc[df["country"] == country]["protein_p"].values[0],
                                      "carbohydrates_p": df.loc[df["country"] == country]["carbohydrates_p"].values[0]}
        
        years[year] = countries
    
    json_object = json.dumps(years, indent=4)

    with open("nutrition_profile_clusters.json", "w") as outfile:
        outfile.write(json_object)
    

if __name__ == "__main__":
    main()