import pandas as pd


def data_summary(filename):
    df = pd.read_csv(
        f"data/4.12.16-5.12.16/{filename}_merged.csv",
        # parse_dates=["ActivityDate"]
    )

    print("Shape:", df.shape)

    print("Columns:", df.dtypes)

    print("Head:", df.head())

    print("Unique Ids:", df["Id"].nunique())


print("-- dailyActivity --")
data_summary("dailyActivity")

print("-- hourlySteps --")
data_summary("hourlySteps")

print("-- hourlyIntensities --")
data_summary("hourlyIntensities")

print("-- hourlyCalories --")
data_summary("hourlyCalories")

print("-- minuteCaloriesNarrow --")
data_summary("minuteCaloriesNarrow")

print("-- minuteIntensitiesNarrow --")
data_summary("minuteIntensitiesNarrow")

print("-- minuteMETsNarrow --")
data_summary("minuteMETsNarrow")
