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
hourlyIntensities_df: DataFrame = pd.read_csv(PATH + "hourlyIntensities_merged.csv")
hourlySteps_df: DataFrame = pd.read_csv(PATH + "hourlySteps_merged.csv")


hourly: DataFrame = merge_dataframes(
    [hourlyCalories_df, hourlyIntensities_df, hourlySteps_df], ["Id", "ActivityHour"]
)

print("-- hourly -- ")
print("Shape:", hourly.shape)
print("Missing values:", hourly.isna().sum())
print("Unique Ids:", hourly["Id"].nunique())

minuteCalories_df: DataFrame = pd.read_csv(PATH + "minuteCaloriesNarrow_merged.csv")
minuteIntensities_df: DataFrame = pd.read_csv(
    PATH + "minuteIntensitiesNarrow_merged.csv"
)
minuteSteps_df: DataFrame = pd.read_csv(PATH + "minuteMETsNarrow_merged.csv")


minute: DataFrame = merge_dataframes(
    [minuteCalories_df, minuteIntensities_df, minuteSteps_df], ["Id", "ActivityMinute"]
)

print("-- minute -- ")
print("Shape:", minute.shape)
print("Missing values:", minute.isna().sum())
print("Unique Ids:", minute["Id"].nunique())
