import pandas as pd
from pandas import DataFrame


def merge_dataframes(dfs: list[DataFrame], key_values: list[str]) -> DataFrame:
    first: DataFrame = dfs[0]
    second: DataFrame = dfs[1]
    third: DataFrame = dfs[2]

    df = first.merge(second, on=key_values, how="outer", validate="one_to_one").merge(
        third, on=key_values, how="outer", validate="one_to_one"
    )

    return df


PATH = "data/4.12.16-5.12.16/"

hourlyCalories_df: DataFrame = pd.read_csv(PATH + "hourlyCalories_merged.csv")
hourlyCalories_df["Date"] = pd.to_datetime(
    hourlyCalories_df["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p"
)
hourlyCalories_df = hourlyCalories_df.drop(columns="ActivityHour")

hourlyIntensities_df: DataFrame = pd.read_csv(PATH + "hourlyIntensities_merged.csv")
hourlyIntensities_df["Date"] = pd.to_datetime(
    hourlyIntensities_df["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p"
)
hourlyIntensities_df = hourlyIntensities_df.drop(columns="ActivityHour")

hourlySteps_df: DataFrame = pd.read_csv(PATH + "hourlySteps_merged.csv")
hourlySteps_df["Date"] = pd.to_datetime(
    hourlySteps_df["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p"
)
hourlySteps_df = hourlySteps_df.drop(columns="ActivityHour")

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

minuteCalories_df: DataFrame = pd.read_csv(PATH + "minuteCaloriesNarrow_merged.csv")
minuteCalories_df["Date"] = pd.to_datetime(
    minuteCalories_df["ActivityMinute"], format="%m/%d/%Y %I:%M:%S %p"
)
minuteCalories_df = minuteCalories_df.drop(columns="ActivityMinute")

minuteIntensities_df: DataFrame = pd.read_csv(
    PATH + "minuteIntensitiesNarrow_merged.csv"
)
minuteIntensities_df["Date"] = pd.to_datetime(
    minuteIntensities_df["ActivityMinute"], format="%m/%d/%Y %I:%M:%S %p"
)
minuteIntensities_df = minuteIntensities_df.drop(columns="ActivityMinute")

minuteMETsNarrow_df: DataFrame = pd.read_csv(PATH + "minuteMETsNarrow_merged.csv")
minuteMETsNarrow_df["Date"] = pd.to_datetime(
    minuteMETsNarrow_df["ActivityMinute"], format="%m/%d/%Y %I:%M:%S %p"
)
minuteMETsNarrow_df = minuteMETsNarrow_df.drop(columns="ActivityMinute")

minute: DataFrame = merge_dataframes(
    [minuteCalories_df, minuteIntensities_df, minuteMETsNarrow_df],
    ["Id", "Date"],
)

print("-- minute -- ")
print("Shape:", minute.shape)
print("Missing values:", minute.isna().sum())
print("Unique Ids:", minute["Id"].nunique())
print("Min, Max Date:", hourly["Date"].agg(["min", "max"]))
print("Months:", hourly["Date"].dt.month.unique())
print("Unique hours:", hourly["Date"].dt.hour.unique())

dailyActivity_df: DataFrame = pd.read_csv(PATH + "dailyActivity_merged.csv")
dailyActivity_df["Date"] = pd.to_datetime(
    dailyActivity_df["ActivityDate"], format="%m/%d/%Y"
)
dailyActivity_df = dailyActivity_df.drop(columns="ActivityDate")

print("-- dailyActivity -- ")
print("Shape:", dailyActivity_df.shape)
print("Missing values:", dailyActivity_df.isna().sum())
print("Unique Ids:", dailyActivity_df["Id"].nunique())
print("Min, Max Date:", hourly["Date"].agg(["min", "max"]))
print("Months:", hourly["Date"].dt.month.unique())
print("Unique hours:", hourly["Date"].dt.hour.unique())


sleepDay_df: DataFrame = pd.read_csv(PATH + "sleepDay_merged.csv")
sleepDay_df["Date"] = pd.to_datetime(sleepDay_df["SleepDay"], format="%m/%d/%Y %I:%M:%S %p")
sleepDay_df = sleepDay_df.drop(columns="SleepDay")

print("-- sleepDay -- ")
print("Shape:", sleepDay_df.shape)
print("Missing values:", sleepDay_df.isna().sum())
print("Unique Ids:", sleepDay_df["Id"].nunique())
print("Min, Max Date:", hourly["Date"].agg(["min", "max"]))
print("Months:", hourly["Date"].dt.month.unique())
print("Unique hours:", hourly["Date"].dt.hour.unique())
