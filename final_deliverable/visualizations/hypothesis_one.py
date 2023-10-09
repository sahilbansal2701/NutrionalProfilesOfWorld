from utils import *
import random
import numpy as np
import pandas as pd

# import matplotlib - very important
import matplotlib.pyplot as plt

# import the toolkit for plotting matplotlib 3D
from mpl_toolkits import mplot3d

# import the stuff for geographic plots
import plotly.figure_factory as ff
import json

def plot_bar_fat(data):

    years = data.keys()
    gdp_high = []
    gdp_low = []

    for key in years:
        gdp_high.append(data[key]["gdp_high"])
        gdp_low.append(data[key]["gdp_low"])

    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))

    br1 = np.arange(len(gdp_low))
    br2 = [x + barWidth for x in br1]

    plt.bar(br1, gdp_low, color ='#ff924e', width = barWidth,
            edgecolor ='grey', label ='Below GDP Threshold*')
    plt.bar(br2, gdp_high, color ='#7fac46', width = barWidth,
            edgecolor ='grey', label ='Above GDP Threshold*')
    
    plt.xlabel('Year', fontweight ='bold', fontsize = 15)
    plt.ylabel('Mean Fat Percentage of Nutritional Profile', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(gdp_low))], years)
    plt.figtext(0.12,0.03, "*GDP Threshold (per capita purchasing power parity 2017): $22,855", ha="left", va="top", fontsize=10)
    plt.title('Mean Fat Percentage According to GDP Threshold Per Year')
    plt.legend(loc='upper center', bbox_to_anchor=(0.913,1.1))
    plt.show()

if __name__ == "__main__":
    data_path = '../hypothesis_one.json'
    with open(data_path) as json_file:
        data = json.load(json_file)
    
    plot_bar_fat(data)