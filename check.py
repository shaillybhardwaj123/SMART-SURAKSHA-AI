
import pandas as pd

df = pd.read_csv("dataset_traffic_accident_prediction1.csv")

print(df.columns)
print(df.head())
print(df.isna().sum())