import pandas as pd
from data_collection import load_data
from preprocessing import clean_data, engineer_features
from eda import analyze_data, plot_insights
from model import evaluate_model,train_model

print('ETHEREUM WHALE TRANSACTION ANALYSIS')

print('\nTask 1 : Load dataset...')
df = load_data()
print("Columns : ",df.columns.tolist())

print("\nTask 2 : Cleaning data")
df = clean_data(df)
df = engineer_features(df)

print("\nTask 3 : Exploratory analysis")
stats = analyze_data(df)
print("Found : ",len(stats)," insights")

print("Task 4 : Visualization")
plot_insights(df)

print("Task 5 : Model")
model = train_model(df)
results = evaluate_model(model,df)
print("Accuracy : ",results['accuracy'])