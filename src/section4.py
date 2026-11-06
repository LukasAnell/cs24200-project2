from pandas import DataFrame, Series
from scipy import stats

from process import build_hourly

ALPHA = 0.05


def add_groups(df: DataFrame) -> DataFrame:
    hour = df["Date"].dt.hour
    day_of_month = df["Date"].dt.day

    return df.assign(
        Hour=hour,
        Period=hour.map(
            lambda h: "night" if h >= 22 or h < 6 else "day"
        ),  # 22:00 to 06:00 is night
        Parity=day_of_month.map(lambda d: "odd" if d % 2 == 1 else "even"),
    )


def user_means(df: DataFrame, group_col: str) -> DataFrame:
    grouped = df.groupby(["Id", group_col])["Calories"].mean()

    return (
        DataFrame(grouped)
        .reset_index()
        .pivot(index="Id", columns=group_col, values="Calories")
    )
