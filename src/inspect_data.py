import pandas as pd

dailyActivity_merged = pd.read_csv(
    "data/4.12.16-5.12.16/dailyActivity_merged.csv",
    # parse_dates=["ActivityDate"]
)

print("Shape:", dailyActivity_merged.shape)

print("Columns:", dailyActivity_merged.dtypes)

print("Head:", dailyActivity_merged.head())

print("Unique Ids:", dailyActivity_merged["Id"].nunique())
