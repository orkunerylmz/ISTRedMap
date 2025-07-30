import pandas as pd
import numpy as np


data = pd.read_csv('data.csv')

def information(df):
    print(df.head())
    print(df.columns)
    print(df.info())
    print(df.shape)
    print(df.duplicated().sum())


def check_missing(df):
    missing_values = df.isnull().sum()
    return print(missing_values)


def missing_rows(df):  
    rows = df[df.isnull().any(axis = 1)]
    
    return print(rows)

def fill_missing_values(df, col, value):
    df.fillna({col: value}, inplace = True)
    return df


def update_format(df, col):
    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S')
    return df


def unique_values(df, col):
    return print(df[col].unique())


def filtered_data(df, col, value):
    return df[df[col] == value]


information(df = data)

data.drop('CLOSED_LANE', axis=1, inplace=True)

check_missing(df = data)
missing_rows(df = data)
fill_missing_values(df=data, col = "ANNOUNCEMENT_TITLE", value = "NO TİTLE")


date_cols = ["ANNOUNCEMENT_STARTING_DATETIME", "ANNOUNCEMENT_ENDING_DATETIME", "INTERVENTION_DATETIME"]

for col in date_cols:
    data[col] = data[col].str.replace('T', ' ')
    data = update_format(df = data, col = col)


unique_values(df = data, col = "ANNOUNCEMENT_TYPE_DESC")

data = filtered_data(df = data, col = "ANNOUNCEMENT_TYPE_DESC", value = "Kaza Bildirimi")

data = data[(data['LATITUDE'] >= 40.5) & (data['LATITUDE'] <= 41.5) & (data['LONGITUDE'] >= 28.5) & (data['LONGITUDE'] <= 29.5)]

data.to_csv("cleaned_data.csv", index=False)

print("Cleaned dataset has been successfully saved as 'cleaned_data.csv' in the current directory.")





