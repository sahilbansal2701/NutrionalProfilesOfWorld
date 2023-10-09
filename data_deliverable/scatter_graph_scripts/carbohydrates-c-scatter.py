#!/usr/bin/env python
import sqlite3
import numpy as np
from matplotlib import pyplot as plt

conn = sqlite3.connect("data/4-move_units/data.db")
c = conn.cursor()

# get country array [Afghanistan, ..., Zimbabwe]
c.execute("SELECT DISTINCT country FROM daily_caloric_supply_derived_from_carbohydrates_protein_and_fat ORDER BY country ASC")
countries = [s[0] for s in c.fetchall()]

# get meat and year array [1961, .., 2013] for each country, and plot
for count in countries:
    # print(count)
    c.execute("SELECT carbohydrates_c, year FROM daily_caloric_supply_derived_from_carbohydrates_protein_and_fat WHERE country = ? AND year BETWEEN 2000 and 2013 ORDER BY year ASC", (count,))
    lst_tuples = c.fetchall()
    carbohydrates_c = [s[0] for s in lst_tuples]
    years = [s[1] for s in lst_tuples]
    plt.plot(years, carbohydrates_c, label = count, linestyle= '-')

plt.legend()
plt.show()



