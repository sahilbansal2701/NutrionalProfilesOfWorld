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
import country_converter as coco
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px

def plot_country_correlation(data):
    """
    """
    countries = data.keys()
    correlation = []
    
    for key in countries:
        correlation.append(data[key]["correlation"])

    iso_3 = coco.convert(names=countries, to='ISO3')

    df = pd.DataFrame({
                "countries": iso_3,
                "correlation": correlation
            })

    fig = px.choropleth(df, locations='countries',
                        color='correlation', # lifeExp is a column of gapminder
                        hover_name='countries', # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title = 'Correlation Between Daily Alcohol Consumption and Life Expectancy For Each Country')
    fig.show()


if __name__ == "__main__":
    data_path = '../hypothesis_two_per_country.json'
    with open(data_path) as json_file:
        data = json.load(json_file)
    
    plot_country_correlation(data)