import pandas as pd


def data_summary(filename, key_cols):
    df = pd.read_csv(
        f"data/4.12.16-5.12.16/{filename}_merged.csv",
        # parse_dates=["ActivityDate"]
    )

    print("Shape:", df.shape)

    print("Columns:", df.dtypes)

    print("Head:", df.head())

    print("Unique Ids:", df["Id"].nunique())

    print("Describe:", df["Id"].value_counts(dropna=False).describe())

    print("Missing Values:", df.isna().sum())

    print("Duplicate count:", df.duplicated(subset=key_cols).sum())


print("-- dailyActivity --")
data_summary("dailyActivity", ["Id", "ActivityDate"])

print("-- hourlySteps --")
data_summary("hourlySteps", ["Id", "ActivityHour"])

print("-- hourlyIntensities --")
data_summary("hourlyIntensities", ["Id", "ActivityHour"])

print("-- hourlyCalories --")
data_summary("hourlyCalories", ["Id", "ActivityHour"])

print("-- minuteCaloriesNarrow --")
data_summary("minuteCaloriesNarrow", ["Id", "ActivityMinute"])

print("-- minuteIntensitiesNarrow --")
data_summary("minuteIntensitiesNarrow", ["Id", "ActivityMinute"])

print("-- minuteMETsNarrow --")
data_summary("minuteMETsNarrow", ["Id", "ActivityMinute"])

print("-- sleepDay --")
data_summary("sleepDay", ["Id", "SleepDay"])

print("-- weightLogInfo --")
data_summary("weightLogInfo", ["Id", "Date"])

print("-- heartrate_seconds --")
data_summary("heartrate_seconds", ["Id", "Time"])
