import pandas as pd
import numpy as np
import random

#################### HELPER FUNCTIONS ####################

RANDOM_SEED = 0
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def train_test_split(df, train_pct=0.8):
    """
    Input:
        - df: Pandas DataFrame
        - train_pct: optional, float
    Output:
        - train dataframe: Pandas DataFrame
        - test dataframe: Pandas DataFrame
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    msk = np.random.rand(len(df)) < train_pct
    return df[msk], df[~msk]

def k_fold_cross_validation_split(df, k):
    """
    Input:
        - df: Pandas DataFrame
        - k: number of folds, int
    Output:
        - k folds dataframe: list of Pandas DataFrames
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    folds = []
    random_fields = np.random.rand(len(df))
    for i in range(k):
        msk = ((i/k) < random_fields) & (random_fields < ((i + 1)/k))
        folds.append(df[msk])
    return folds

def drop_incomplete_rows(df):
    """
    Input:
        - df: Pandas DataFrame
    Output:
        - a Pandas DataFrame where all rows no longer
        contain null values or empty strings
    """
    columns = df.columns
    def row_complete(row):
        for col in columns:
            val = row[col]
            nan = pd.isnull(val)
            str_empty = type(val) == str and val.strip() == ""
            if nan or str_empty:
                return False
        return True
    return df[df.apply(lambda x: row_complete(x), axis=1)]

def print_dict_years1(stats):
    for key in stats.keys():
        print(key, stats.get(key))

def print_dict_years2(stats):
    for key in stats.keys():
        print(key, end=": ")
        for key1 in stats.get(key):
            print(key1, ":", stats.get(key).get(key1), end=", ")
        print()

def list_to_string(lst):
    output = ""
    for i in lst:
        output += i + ", "
    return output[:-2]