#!/usr/bin/env python

import sqlite3
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
from scipy import stats
from util import drop_incomplete_rows, train_test_split, k_fold_cross_validation_split, list_to_string
from sklearn.metrics import r2_score


database_path = "data/9-percentages/data.db"
MAX_CLUSTERS = 20
cmap = cm.get_cmap('tab10', MAX_CLUSTERS)


def visualize_r2(degree, r2):
    plt.clf()
    plt.plot(degree, r2)
    plt.xlabel('Degree')
    plt.ylabel('R-Squared Value')
    plt.show()


def visualize_nutrition_clusters(data, annotations, centroids=None, centroid_indices=None, annotate=False):
    x, y, z = np.hsplit(data, 3)
    def plot_profiles(fig, color_map=None):
        fig.scatter(x, y, z, c=color_map)

    def plot_clusters(fig):
        x, y, z = np.hsplit(centroids, 3)
        fig.scatter(x, y, z, c="black", marker="x", alpha=1, s=200)

    plt.clf()
    cluster_plot = centroids is not None and centroid_indices is not None

    ax = plt.figure(num=1).add_subplot(111, projection='3d')
    colors_s = None

    if cluster_plot:
        if max(centroid_indices) + 1 > MAX_CLUSTERS:
            print(f"Error: Too many clusters. Please limit to fewer than {MAX_CLUSTERS}.")
            exit(1)
        colors_s = [cmap(l / MAX_CLUSTERS) for l in centroid_indices]
        plot_clusters(ax)

    plot_profiles(ax, colors_s)

    ax.set_xlabel("fat_c")
    ax.set_ylabel("protein_c")
    ax.set_zlabel("carbohydrates_c")

    if annotate:
        for i in range(data.shape[0]):
            ax.text(data["fat_c"][i], data["protein_c"][i], data["carbohydrates_c"][i], annotations[i])
    
    # Helps visualize clusters
    plt.gca().invert_xaxis()
    plt.show()


def euclidean_dist(x, y):
    """
    Computes the Euclidean distance between two points, x and y

    :param x: the first data point, a Python numpy array
    :param y: the second data point, a Python numpy array
    :return: the Euclidean distance between x and y
    """
    return np.linalg.norm(x - y)


def inertia(data, centroids, centroid_indices):
    """
    Returns the inertia of the clustering. Inertia is defined as the
    sum of the squared distances between each data point and the centroid of
    its assigned cluster.

    :param centroids - the coordinates that represent the center of the clusters
    :param centroid_indices - the index of the centroid that corresponding data point it closest to
    :return inertia as a float
    """
    intertia = 0.0
    for i, point in enumerate(data):
        dist = euclidean_dist(point, centroids[centroid_indices[i]])
        intertia += dist * dist
    print(type(intertia))
    return intertia    


def elbow_point_plot(cluster, errors):
    plt.clf()
    plt.plot(cluster, errors)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.show()


def concatenate_data(df, i):
    first_run = True
    for k in range(len(df)):
        if (k != i):
            if first_run:
                training_data = df[k]
            else:
                pd.concat([training_data, df[k]])
    return training_data


def ml_model_1(validation):
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Get All Data for GDP and FAT
    c.execute("SELECT gdp_per_capita_ppp_2017, (CAST(fat_c AS FLOAT)/(meat_protein_c + plant_protein_c + carbohydrates_c + fat_c) * 100) FROM diet_and_life")
    lst_tuples = c.fetchall()
    regression_x = [s[0] for s in lst_tuples]
    regression_y = [s[1] for s in lst_tuples]

    # Turn into Dataframe
    df = pd.DataFrame({
        "gdp": regression_x,
        "fat": regression_y
    })
    df = drop_incomplete_rows(df)

    # Split Data
    train, test = train_test_split(df)

    # Runs Validation
    if (validation == True):
        k_folds = 5
        dataframes = k_fold_cross_validation_split(df, k_folds)
        r2 = []
        degree = []
        for deg in range(8):
            print("Degree:", deg)
            old_r2 = []
            for i in range(k_folds):
                validation = dataframes[i]
                training_data = concatenate_data(dataframes, i)
                coefficients_val = np.polyfit(training_data["gdp"].values.tolist(), training_data["fat"].values.tolist(), deg)
                predictions = np.polyval(coefficients_val, validation["gdp"].values.tolist())
                rsquared_val = r2_score(validation["fat"].values.tolist(), predictions)
                old_r2.append(rsquared_val)
                print("FOLD:", i, " | R-SQUARED:", rsquared_val )
            avg_r2 = np.average(old_r2)
            print("AVERAGE R-SQUARED:", avg_r2)
            r2.append(avg_r2)
            degree.append(deg)
        visualize_r2(degree, r2)
    else:
        degree = []
        parameters = []
        r2 = [] 
        for i in range(8):
            coefficients = np.polyfit(train["gdp"].values.tolist(), train["fat"].values.tolist(), i)
            predictions = np.polyval(coefficients, test["gdp"].values.tolist())
            rsquared_val = r2_score(test["fat"].values.tolist(), predictions)
            print("Degree:", i, "R2:", rsquared_val)
            degree.append(i)
            parameters.append(coefficients)
            r2.append(rsquared_val)
        visualize_r2(degree, r2)


def ml_model_2():
    # Connect to Database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    for year in range(2000, 2014, 1):
        print("Year: " + str(year))
        c.execute("SELECT fat_c, meat_protein_c + plant_protein_c, carbohydrates_c, country FROM diet_and_life WHERE year = " + str(year))
        lst_tuples = c.fetchall()
        df = pd.DataFrame({
            "fat_c": [s[0] for s in lst_tuples],
            "protein_c": [s[1] for s in lst_tuples],
            "carbohydrates_c": [s[2] for s in lst_tuples],
            "country": [s[3] for s in lst_tuples],
        })
        df = drop_incomplete_rows(df)
        visualize_nutrition_clusters(df[["fat_c", "protein_c", "carbohydrates_c"]], df["country"], False)
        cluster = [i for i in range(1, MAX_CLUSTERS+1)]
        errors = []
        for k in cluster:
            kmeans = KMeans(n_clusters=k, n_init='auto').fit(df[["fat_c", "protein_c", "carbohydrates_c"]])
            errors.append(kmeans.inertia_)
        elbow_point_plot(cluster, errors)

        visualize_nutrition_clusters(df[["fat_c", "protein_c", "carbohydrates_c"]], df["country"], kmeans.cluster_centers_, kmeans.labels_, False)

        for j in range(k):
            mask = kmeans.labels_ == j
            print("Cluster " + str(j) + ": " + list_to_string(df["country"][mask].tolist()))


def main():  
    print("Running ML Model 1: With Validation")
    ml_model_1(True)  
    print("----------------------------------")
    print("Running ML Model 1: Without Validation")
    ml_model_1(False)
    print("----------------------------------")
    print("Running ML Model 2")
    ml_model_2()
    print("----------------------------------")
    

if __name__ == "__main__":
    main()