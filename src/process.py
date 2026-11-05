import pandas as pd
from pandas import DataFrame

PATH = "data/4.12.16-5.12.16/"
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"


def merge_dataframes(dfs: list[DataFrame], key_values: list[str]) -> DataFrame:
    first: DataFrame = dfs[0]
    second: DataFrame = dfs[1]
    third: DataFrame = dfs[2]

    df = first.merge(second, on=key_values, how="outer", validate="one_to_one").merge(
        third, on=key_values, how="outer", validate="one_to_one"
    )

    return df


def load_with_date(filename: str, column: str, fmt: str) -> DataFrame:
    df: DataFrame = pd.read_csv(PATH + filename)
    df["Date"] = pd.to_datetime(df[column], format=fmt)
    return df.drop(columns=column)


hourlyCalories_df = load_with_date(
    "hourlyCalories_merged.csv", "ActivityHour", DATE_FORMAT
)

hourlyIntensities_df = load_with_date(
    "hourlyIntensities_merged.csv", "ActivityHour", DATE_FORMAT
)

hourlySteps_df = load_with_date("hourlySteps_merged.csv", "ActivityHour", DATE_FORMAT)

hourly: DataFrame = merge_dataframes(
    [hourlyCalories_df, hourlyIntensities_df, hourlySteps_df], ["Id", "Date"]
)

print("-- hourly -- ")
print("Shape:", hourly.shape)
print("Missing values:", hourly.isna().sum())
print("Unique Ids:", hourly["Id"].nunique())
print("Min, Max Date:", hourly["Date"].agg(["min", "max"]))
print("Months:", hourly["Date"].dt.month.unique())
print("Unique hours:", hourly["Date"].dt.hour.unique())
print(hourly[hourly["Date"].dt.hour.isin([0, 12])].head(4))


minuteCalories_df = load_with_date(
    "minuteCaloriesNarrow_merged.csv", "ActivityMinute", DATE_FORMAT
)

minuteIntensities_df = load_with_date(
    "minuteIntensitiesNarrow_merged.csv", "ActivityMinute", DATE_FORMAT
)

minuteMETsNarrow_df = load_with_date(
    "minuteMETsNarrow_merged.csv", "ActivityMinute", DATE_FORMAT
)

minute: DataFrame = merge_dataframes(
    [minuteCalories_df, minuteIntensities_df, minuteMETsNarrow_df],
    ["Id", "Date"],
)

print("-- minute -- ")
print("Shape:", minute.shape)
print("Missing values:", minute.isna().sum())
print("Unique Ids:", minute["Id"].nunique())
print("Min, Max Date:", minute["Date"].agg(["min", "max"]))
print("Months:", minute["Date"].dt.month.unique())
print("Unique hours:", minute["Date"].dt.hour.unique())
print(minute[minute["Date"].dt.hour.isin([0, 12])].head(4))

dailyActivity_df = load_with_date(
    "dailyActivity_merged.csv", "ActivityDate", "%m/%d/%Y"
)

print("-- dailyActivity -- ")
print("Shape:", dailyActivity_df.shape)
print("Missing values:", dailyActivity_df.isna().sum())
print("Unique Ids:", dailyActivity_df["Id"].nunique())
print("Min, Max Date:", dailyActivity_df["Date"].agg(["min", "max"]))
print("Months:", dailyActivity_df["Date"].dt.month.unique())
print("Unique hours:", dailyActivity_df["Date"].dt.hour.unique())

sleepDay_df = load_with_date("sleepDay_merged.csv", "SleepDay", DATE_FORMAT)

print("-- sleepDay -- ")
print("Shape:", sleepDay_df.shape)
print("Missing values:", sleepDay_df.isna().sum())
print("Unique Ids:", sleepDay_df["Id"].nunique())
print("Min, Max Date:", sleepDay_df["Date"].agg(["min", "max"]))
print("Months:", sleepDay_df["Date"].dt.month.unique())
print("Unique hours:", sleepDay_df["Date"].dt.hour.unique())
