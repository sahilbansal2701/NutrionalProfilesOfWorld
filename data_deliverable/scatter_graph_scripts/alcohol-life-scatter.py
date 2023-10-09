#!/usr/bin/env python
import sqlite3
import numpy as np
from matplotlib import pyplot as plt

conn = sqlite3.connect("data\8-aggregate\data.db")
c = conn.cursor()

# get country array [Afghanistan, ..., Zimbabwe]
c.execute("SELECT DISTINCT country FROM diet_and_life ORDER BY country ASC")
countries = [s[0] for s in c.fetchall()]

# get alcohol and life array for each country, and plot
for count in countries:
    # print(count)
    c.execute("SELECT alcohol_c_pp_pd, life_expectancy FROM diet_and_life WHERE country = ? AND year BETWEEN 2000 and 2013 ORDER BY year ASC", (count,))
    lst_tuples = c.fetchall()
    alcohol_kc = [s[0] for s in lst_tuples]
    life = [s[1] for s in lst_tuples]
    plt.plot(life, alcohol_kc, label = count, linestyle= '-')

plt.legend()
plt.show()

c.execute("SELECT DISTINCT year FROM diet_and_life ORDER BY year ASC")
years = [s[0] for s in c.fetchall()]

# get alcohol and life array for each year, and plot
for count in years:
    # print(count)
    c.execute("SELECT alcohol_c_pp_pd, life_expectancy FROM diet_and_life WHERE year = ? ORDER BY life_expectancy ASC", (count,))
    lst_tuples = c.fetchall()
    alcohol_kc = [s[0] for s in lst_tuples]
    life = [s[1] for s in lst_tuples]
    plt.plot(life, alcohol_kc, label = count, linestyle= '-')
    plt.legend()
    plt.show()
