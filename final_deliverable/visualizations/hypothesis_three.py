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

def plot_linear_line(data):
    """
    """
    years = data.keys()
    correlation = []
    
    for key in years:
        correlation.append(data[key]["correlation"])

    # alright, scatter plot the points
    fig, ax = plt.subplots(facecolor='#F98D94')
    ax.plot(years, correlation, '-ok')
    ax.set_title('Correlation Between GDP and Meat Consumption For Each Year [2000-2013]')
    ax.set_xlabel('Year')
    ax.set_ylabel('Correlation')
    ax.set_facecolor('#eafff5')
    
    plt.show()

if __name__ == "__main__":
    data_path = '../hypothesis_three_per_year.json'
    with open(data_path) as json_file:
        data = json.load(json_file)
    
    plot_linear_line(data)