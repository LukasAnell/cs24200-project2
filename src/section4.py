from typing import Any

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


def paired_test(means: DataFrame, a: str, b: str, label: str):
    pairs: DataFrame = means.dropna(subset=[a, b])
    x: Series = pairs.loc[:, a]
    y: Series = pairs.loc[:, b]
    diff: Series = x - y

    result = stats.ttest_rel(x, y)
    ci = result.confidence_interval(confidence_level=1 - ALPHA)

    print(f"-- Paired t-test: {label} ({a} - {b}) --")
    print(f"Users with both groups: {len(pairs)} of {len(means)}")
    print(f"Mean calories per hour: {a} = {x.mean():.3f}, {b} = {y.mean():.3f}")
    print(f"Mean difference: {diff.mean():.3f}")
    print(f"95% CI for the mean difference: ({ci.low:.3f}, {ci.high:.3f})")
    print(f"t = {result.statistic:.3f}, df = {result.df:.0f}, p = {result.pvalue:.4g}")
    print(f"Effect size: {diff.mean() / diff.std():.3f}")
    print("Reject H_0 at alpha = 0.05:", result.pvalue < ALPHA)
    print()


def welch_test(df: DataFrame, group_col: str, a: str, b: str, label: str):
    x: Series = df.loc[df[group_col] == a, "Calories"]
    y: Series = df.loc[df[group_col] == b, "Calories"]

    result: Any = stats.ttest_ind(x, y, equal_var=False)
    ci = result.confidence_interval(confidence_level=1 - ALPHA)

    print(f"-- Welch two-sample t-test on all hourly rows: {label} ({a} - {b}) --")
    print(f"n: {a} = {len(x)}, {b} = {len(y)}")
    print(f"Mean calories per hour: {a} = {x.mean():.3f}, {b} = {y.mean():.3f}")
    print(f"Mean difference: {x.mean() - y.mean():.3f}")
    print(f"95% CI for the mean difference: ({ci.low:.3f}, {ci.high:.3f})")
    print(f"t = {result.statistic:.3f}, df = {result.df:.0f}, p = {result.pvalue:.4g}")
    print("Reject H_0 at alpha = 0.05:", result.pvalue < ALPHA)
    print()


def main():
    hourly_df = add_groups(build_hourly())

    print("Rows:", len(hourly_df), "Users:", hourly_df["Id"].nunique())
    print("Missing Calories:", hourly_df["Calories"].isna().sum())
    print(hourly_df["Period"].value_counts())
    print(hourly_df["Parity"].value_counts())
    print()

    day_night = user_means(hourly_df, "Period")
    print(day_night.head())
    paired_test(day_night, "day", "night", "day vs night")

    odd_even = user_means(hourly_df, "Parity")
    paired_test(odd_even, "odd", "even", "odd vs even day")

    welch_test(hourly_df, "Period", "day", "night", "day vs night")
    welch_test(hourly_df, "Parity", "odd", "even", "odd vs even day")


if __name__ == "__main__":
    main()
