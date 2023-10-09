#!/usr/bin/env python
import sqlite3
import numpy as np
from matplotlib import pyplot as plt

conn = sqlite3.connect("data/4-move_units/data.db")
c = conn.cursor()

# get country array [Afghanistan, ..., Zimbabwe]
c.execute("SELECT DISTINCT country FROM dietary_compositions_by_commodity_group ORDER BY country ASC")
countries = [s[0] for s in c.fetchall()]

# get meat and year array [1961, .., 2013] for each country, and plot
for count in countries:
    # print(count)
    c.execute("SELECT alcohol_c_pp_pd, year FROM dietary_compositions_by_commodity_group WHERE country = ? AND year BETWEEN 2000 and 2013 ORDER BY year ASC", (count,))
    lst_tuples = c.fetchall()
    alcohol_kc = [s[0] for s in lst_tuples]
    years = [s[1] for s in lst_tuples]
    plt.plot(years, alcohol_kc, label = count, linestyle= '-')

plt.legend()
plt.show()



