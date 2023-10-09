#!/usr/bin/env python

import numpy as np
import pandas as pd
import random
from util import drop_incomplete_rows, print_dict_years2
from scipy.stats import ttest_1samp, ttest_ind, pearsonr, spearmanr
import sqlite3
import json
from statistics import mean


database_path = "../data/9-percentages/data.db"

def hypothesis_one_fat_c_pp_pd():
    '''
    Title: GDP and Fat
    Hypothesis: We hypothesize that countries with at least a GDP (per capita purchasing 
        power parity 2017) of 22855 will have a diet that consists of at least 11% fat 
        compared to countries with a GDP that is lower than 22855.
    '''

    high_gdp_threshold = "22855"

    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    c.execute("SELECT DISTINCT year FROM diet_and_life ORDER BY year ASC")
    years = [s[0] for s in c.fetchall()]
    stats = {}

    for year in years:
        # For Each Year Get FAT_PERCENTAGED For LOW and HIGH GDP Countries
        c.execute("SELECT fat_percent_pp_pd " + 
                  "FROM diet_and_life " + 
                  "WHERE gdp_per_capita_ppp_2017 > " + high_gdp_threshold + " " + 
                    "AND year = ?", (year,))
        gdp_high = [s[0] for s in c.fetchall()]

        c.execute("SELECT fat_percent_pp_pd " + 
                  "FROM diet_and_life " + 
                  "WHERE gdp_per_capita_ppp_2017 <= " + high_gdp_threshold + " " + 
                    "AND year = ?", (year,))
        gdp_low = [s[0] for s in c.fetchall()]

        # Turn Data into Pandas Dataframe
        df1 = pd.DataFrame({
            "gdp_high": gdp_high
        })
        df2 = pd.DataFrame({
            "gdp_low": gdp_low
        })
        df1 = drop_incomplete_rows(df1)
        df2 = drop_incomplete_rows(df2)

        # Compute Chi^2
        tstats, pvalue = ttest_ind(df1["gdp_high"], df2["gdp_low"])
        stats[year] = {"tstat": tstats, "pvalue": pvalue}
    
    print_dict_years2(stats)


def hypothesis_one_fat_c():
    '''
    Title: GDP and Fat
    Hypothesis: We hypothesize that countries with at least a GDP (per capita purchasing 
        power parity 2017) of 22855 will have a diet that consists of at least 11% fat 
        compared to countries with a GDP that is lower than 22855.
    '''

    high_gdp_threshold = "22855"

    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    c.execute("SELECT DISTINCT year FROM diet_and_life ORDER BY year ASC")
    years = [s[0] for s in c.fetchall()]
    stats = {}
    gdp_fat = {}

    for year in years:
        # For Each Year Get FAT_PERCENTAGED For LOW and HIGH GDP Countries
        c.execute("SELECT (CAST(fat_c AS FLOAT)/(meat_protein_c + plant_protein_c + carbohydrates_c + fat_c) * 100) " + 
                  "FROM diet_and_life " + 
                  "WHERE gdp_per_capita_ppp_2017 > " + high_gdp_threshold + " " + 
                    "AND year = ?", (year,))
        gdp_high = [s[0] for s in c.fetchall()]

        c.execute("SELECT (CAST(fat_c AS FLOAT)/(meat_protein_c + plant_protein_c + carbohydrates_c + fat_c) * 100) " + 
                  "FROM diet_and_life " + 
                  "WHERE gdp_per_capita_ppp_2017 <= " + high_gdp_threshold + " " + 
                    "AND year = ?", (year,))
        gdp_low = [s[0] for s in c.fetchall()]

        # Turn Data into Pandas Dataframe
        df1 = pd.DataFrame({
            "gdp_high": gdp_high
        })
        df2 = pd.DataFrame({
            "gdp_low": gdp_low
        })
        df1 = drop_incomplete_rows(df1)
        df2 = drop_incomplete_rows(df2)

        # Compute Chi^2
        tstats, pvalue = ttest_ind(df1["gdp_high"], df2["gdp_low"])
        stats[year] = {"tstat": tstats, "pvalue": pvalue}
        gdp_fat[year] = {'gdp_high': mean(gdp_high), 'gdp_low' : mean(gdp_low)}
    
    print_dict_years2(stats)

    json_object = json.dumps(gdp_fat, indent=4)
    with open("hypothesis_one.json", "w") as outfile:
        outfile.write(json_object)

def hypothesis_two_all_together():
    '''
    Title: Alcohol and Life Expectancy
    Hypothesis: We hypothesize that there will be a 
        negative correlation between alcohol consumption 
        and life expectancy.
    '''
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    stats = {}

    c.execute("SELECT alcohol_c_pp_pd, life_expectancy FROM diet_and_life")
    lst_tuples = c.fetchall()
    alcohol = [s[0] for s in lst_tuples]
    life_expectancy = [s[1] for s in lst_tuples]

    # Turn Data into Pandas Dataframe
    df = pd.DataFrame({
        "alcohol": alcohol,
        "life_expectancy": life_expectancy
    })

    df = drop_incomplete_rows(df)
    # result = pearsonr(df["alcohol"], df["life_expectancy"], alternative='less')
    result = spearmanr(df["alcohol"], df["life_expectancy"], alternative='less')
    print("correlation: " + str(result.statistic) + ", pvalue: " + str(result.pvalue))


def hypothesis_two_per_country(): 
    '''
    Title: Alcohol and Life Expectancy
    Hypothesis: We hypothesize that there will be a 
        negative correlation between alcohol consumption 
        and life expectancy.
    '''
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    c.execute("SELECT DISTINCT country FROM diet_and_life ORDER BY country ASC")
    countries = [s[0] for s in c.fetchall()]
    stats = {}

    for country in countries:
        # For Each Year Get alcohol_c_pp_pd and life_expectancy
        c.execute("SELECT alcohol_c_pp_pd, life_expectancy FROM diet_and_life WHERE country = ?", (country,))
        lst_tuples = c.fetchall()
        alcohol = [s[0] for s in lst_tuples]
        life_expectancy = [s[1] for s in lst_tuples]

        # Turn Data into Pandas Dataframe
        df = pd.DataFrame({
            "alcohol": alcohol,
            "life_expectancy": life_expectancy
        })

        df = drop_incomplete_rows(df)
        if df.shape[0] > 1:
            # result = pearsonr(df["alcohol"], df["life_expectancy"], alternative='less')
            result = spearmanr(df["alcohol"], df["life_expectancy"], alternative='less')
            stats[country] = {"correlation": result.statistic, "pvalue": result.pvalue}

    json_object = json.dumps(stats, indent=4)
    with open("hypothesis_two_per_country.json", "w") as outfile:
        outfile.write(json_object)

    print_dict_years2(stats)

    


def hypothesis_two_per_year():
    '''
    Title: Alcohol and Life Expectancy
    Hypothesis: We hypothesize that there will be a 
        negative correlation between alcohol consumption 
        and life expectancy.
    '''
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    c.execute("SELECT DISTINCT year FROM diet_and_life ORDER BY year ASC")
    years = [s[0] for s in c.fetchall()]
    stats = {}
    corr = []

    for year in years:
        # For Each Year Get alcohol_c_pp_pd and life_expectancy
        c.execute("SELECT alcohol_c_pp_pd, life_expectancy FROM diet_and_life WHERE year = ?", (year,))
        lst_tuples = c.fetchall()
        alcohol = [s[0] for s in lst_tuples]
        life_expectancy = [s[1] for s in lst_tuples]

        # Turn Data into Pandas Dataframe
        df = pd.DataFrame({
            "alcohol": alcohol,
            "life_expectancy": life_expectancy
        })

        df = drop_incomplete_rows(df)
        # result = pearsonr(df["alcohol"], df["life_expectancy"], alternative='less')
        result = spearmanr(df["alcohol"], df["life_expectancy"], alternative='less')
        stats[year] = {"correlation": result.statistic, "pvalue": result.pvalue}
        corr.append(result.statistic)

    print_dict_years2(stats)

    tstat, pvalue = ttest_1samp(corr, 0, alternative='less')
    return pvalue


def hypothesis_three_all_together(): 
    '''
    Title: GDP and Meat
    Hypothesis: We hypothesize that there is a positive correlation between 
        GDP and the amount of meat consumed in a country.
    ''' 
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    stats = {}

    c.execute("SELECT gdp_per_capita_ppp_2017, meat_protein_c FROM diet_and_life")
    lst_tuples = c.fetchall()
    gdp = [s[0] for s in lst_tuples]
    meat_protein_c = [s[1] for s in lst_tuples]

    # Turn Data into Pandas Dataframe
    df = pd.DataFrame({
        "gdp": gdp,
        "meat": meat_protein_c
    })

    df = drop_incomplete_rows(df)
    # result = pearsonr(df["gdp"], df["meat"], alternative='greater')
    result = spearmanr(df["gdp"], df["meat"], alternative='greater')
    print("correlation: " + str(result.statistic) + ", pvalue: " + str(result.pvalue))    


def hypothesis_three_per_country(): 
    '''
    Title: GDP and Meat
    Hypothesis: We hypothesize that there is a positive correlation between 
        GDP and the amount of meat consumed in a country.
    ''' 
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    c.execute("SELECT DISTINCT country FROM diet_and_life ORDER BY country ASC")
    countries = [s[0] for s in c.fetchall()]
    stats = {}

    for country in countries:
        # For Each Year Get GDP and Meat_Protien_C
        c.execute("SELECT gdp_per_capita_ppp_2017, meat_protein_c FROM diet_and_life WHERE country = ?", (country,))
        lst_tuples = c.fetchall()
        gdp = [s[0] for s in lst_tuples]
        meat_protein_c = [s[1] for s in lst_tuples]

        # Turn Data into Pandas Dataframe
        df = pd.DataFrame({
            "gdp": gdp,
            "meat": meat_protein_c
        })
        df = drop_incomplete_rows(df)
        if df.shape[0] > 1:
            # result = pearsonr(df["gdp"], df["meat"], alternative='greater')
            result = spearmanr(df["gdp"], df["meat"], alternative='greater')
            stats[country] = {"correlation": result.statistic, "pvalue": result.pvalue}

    print_dict_years2(stats)


def hypothesis_three_per_year(): 
    '''
    Title: GDP and Meat
    Hypothesis: We hypothesize that there is a positive correlation between 
        GDP and the amount of meat consumed in a country.
    ''' 
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Distinct Years
    c.execute("SELECT DISTINCT year FROM diet_and_life ORDER BY year ASC")
    years = [s[0] for s in c.fetchall()]
    stats = {}
    corr = []

    for year in years:
        # For Each Year Get GDP and Meat_Protien_C
        c.execute("SELECT gdp_per_capita_ppp_2017, meat_protein_c FROM diet_and_life WHERE year = ?", (year,))
        lst_tuples = c.fetchall()
        gdp = [s[0] for s in lst_tuples]
        meat_protein_c = [s[1] for s in lst_tuples]

        # Turn Data into Pandas Dataframe
        df = pd.DataFrame({
            "gdp": gdp,
            "meat": meat_protein_c
        })

        df = drop_incomplete_rows(df)
        # result = pearsonr(df["gdp"], df["meat"], alternative='greater')
        result = spearmanr(df["gdp"], df["meat"], alternative='greater')
        stats[year] = {"correlation": result.statistic, "pvalue": result.pvalue}
        corr.append(result.statistic)

    json_object = json.dumps(stats, indent=4)
    with open("hypothesis_three_per_year.json", "w") as outfile:
        outfile.write(json_object)

    print_dict_years2(stats)

    tstat, pvalue = ttest_1samp(corr, 0, alternative='greater')
    return pvalue


if __name__ == "__main__":
    random.seed()

    print("Running Test for Hypothesis 1: P-value from 2-Sample TTest: fat_c_pp_pd")
    hypothesis_one_fat_c_pp_pd()
    print("------------------------------")
    print("Running Test for Hypothesis 1: P-value from 2-Sample TTest: fat_c")
    hypothesis_one_fat_c()
    print("------------------------------")

    print("Running Test for Hypothesis 2: P-value per Country (Spearman)")
    hypothesis_two_per_country()
    print("------------------------------")
    print("Running Test for Hypothesis 2: P-value per Year (Spearman)")
    pval_ttest = hypothesis_two_per_year()
    print("------------------------------")
    print("Running Test for Hypothesis 2: All Together P-value (Spearman)")
    hypothesis_two_all_together()
    print("------------------------------")
    print("Running Test for Hypothesis 2: All Together P-value (1-Sample TTest)")
    print("P-Value: " + str(pval_ttest))
    print("------------------------------")

    print("Running Test for Hypothesis 3: P-value per Country (Spearman)")
    hypothesis_three_per_country()
    print("------------------------------")
    print("Running Test for Hypothesis 3: P-value per Year (Spearman)")
    pval_ttest = hypothesis_three_per_year()
    print("------------------------------")
    print("Running Test for Hypothesis 3: All Together P-value (Spearman)")
    hypothesis_three_all_together()
    print("------------------------------")
    print("Running Test for Hypothesis 3: All Together P-value (1-Sample TTest)")
    print("P-Value: " + str(pval_ttest))
    print("------------------------------")