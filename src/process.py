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


def build_hourly() -> DataFrame:
    hourlyCalories_df = load_with_date(
        "hourlyCalories_merged.csv", "ActivityHour", DATE_FORMAT
    )
    hourlyIntensities_df = load_with_date(
        "hourlyIntensities_merged.csv", "ActivityHour", DATE_FORMAT
    )
    hourlySteps_df = load_with_date(
        "hourlySteps_merged.csv", "ActivityHour", DATE_FORMAT
    )

    return merge_dataframes(
        [hourlyCalories_df, hourlyIntensities_df, hourlySteps_df], ["Id", "Date"]
    )


def build_minute() -> DataFrame:
    minuteCalories_df = load_with_date(
        "minuteCaloriesNarrow_merged.csv", "ActivityMinute", DATE_FORMAT
    )
    minuteIntensities_df = load_with_date(
        "minuteIntensitiesNarrow_merged.csv", "ActivityMinute", DATE_FORMAT
    )
    minuteMETsNarrow_df = load_with_date(
        "minuteMETsNarrow_merged.csv", "ActivityMinute", DATE_FORMAT
    )

    return merge_dataframes(
        [minuteCalories_df, minuteIntensities_df, minuteMETsNarrow_df], ["Id", "Date"]
    )


def load_daily_activity() -> DataFrame:
    return load_with_date("dailyActivity_merged.csv", "ActivityDate", "%m/%d/%Y")


def load_sleep() -> DataFrame:
    return load_with_date("sleepDay_merged.csv", "SleepDay", DATE_FORMAT)


def build_heartrate() -> DataFrame:
    df = load_with_date("heartrate_seconds_merged.csv", "Time", DATE_FORMAT)
    df["Date"] = df["Date"].dt.floor("min")
    return DataFrame(df.groupby(["Id", "Date"], as_index=False)["Value"].mean())


def summarize(name, df):
    print(f"-- {name} -- ")
    print("Shape:", df.shape)
    print("Missing values:", df.isna().sum())
    print("Unique Ids:", df["Id"].nunique())
    print("Min, Max Date:", df["Date"].agg(["min", "max"]))
    print("Months:", df["Date"].dt.month.unique())
    print("Unique hours:", df["Date"].dt.hour.unique())
    print(df[df["Date"].dt.hour.isin([0, 12])].head(4))


def main():
    hourly = build_hourly()
    summarize("hourly", hourly)

    minute = build_minute()
    summarize("minute", minute)

    dailyActivity_df = load_daily_activity()
    summarize("dailyActivity", dailyActivity_df)

    sleepDay_df = load_sleep()
    summarize("sleepDay", sleepDay_df)

    heartrate_df = build_heartrate()
    summarize("heartrate", heartrate_df)


if __name__ == "__main__":
    main()
