import pandas as pd
from data_collection import load_data
from preprocessing import clean_data, engineer_features

print('ETHEREUM WHALE TRANSACTION ANALYSIS')

print('\nTask 1 : Load dataset...')
df = load_data()
print("Columns : ",df.columns.tolist())

print("\nTask 2 : Cleaning data")
df = clean_data(df)
df = engineer_features(df)

