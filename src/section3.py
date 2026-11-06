import numpy as np
from pandas import DataFrame, Series
from plotnine import (
    aes,
    geom_abline,
    geom_col,
    geom_point,
    ggplot,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme_minimal,
)

from process import build_hourly, load_sleep
from section1 import select_users_by_days


def check_intensity_columns(df: DataFrame):
    # AverageIntensity = TotalIntensity / 60
    diff = (df["AverageIntensity"] - df["TotalIntensity"] / 60).abs()

    print("Max |AverageIntensity - TotalIntensity / 60|:", diff.max())
    print(
        "AverageIntensity == TotalIntensity / 60:",
        np.allclose(df["AverageIntensity"], df["TotalIntensity"] / 60, atol=1e-6),
    )


def check_zero_step_outliers(df: DataFrame):
    rows: DataFrame = df.loc[(df["StepTotal"] == 0) & (df["Calories"] > 600)]

    print("0 Steps and Calories > 600:", len(rows))
    print(rows.sort_values(by=["Id", "Date"]))
    print(rows.groupby("Id").size())

    steps: Series = df.loc[:, "StepTotal"]
    intensity: Series = df.loc[:, "TotalIntensity"]
    print("Steps vs intensity r:", round(steps.corr(intensity), 4))


def compare_correlations_without_outliers(df: DataFrame):
    outlier_mask = (df["StepTotal"] == 0) & (df["Calories"] > 600)
    cleaned: DataFrame = df.loc[~outlier_mask]

    print("Rows before/after:", len(df), len(cleaned))

    for col in ["StepTotal", "TotalIntensity"]:
        all_rows: Series = df.loc[:, col]
        all_calories: Series = df.loc[:, "Calories"]

        kept: Series = cleaned.loc[:, col]
        kept_calories: Series = cleaned.loc[:, "Calories"]

        print(
            f"{col}: r with all rows = {all_rows.corr(all_calories):.4f}, "
            f"without outliers = {kept.corr(kept_calories):.4f}"
        )


def plot_scatter(df: DataFrame, x: str, xlabel: str, title: str, filename: str):
    plot = (
        ggplot(df, aes(x=x, y="Calories"))
        + geom_point(alpha=0.15, size=1)
        + labs(title=title, x=xlabel, y="Calories (per hour)")
        + theme_minimal()
    )

    plot.save("figures/" + filename)


def plot_3_1():
    hourly_df = build_hourly()

    print("Shape:", hourly_df.shape)
    print(hourly_df.isna().sum())
    check_intensity_columns(hourly_df)

    plot_scatter(
        hourly_df,
        "StepTotal",
        "Steps (per hour)",
        "Calories vs Steps (hourly)",
        "calories_vs_steps.png",
    )
    plot_scatter(
        hourly_df,
        "TotalIntensity",
        "Total Intensity (per hour)",
        "Calories vs Intensity (hourly)",
        "calories_vs_intensity.png",
    )

    check_zero_step_outliers(hourly_df)
    compare_correlations_without_outliers(hourly_df)

    cols: DataFrame = hourly_df.loc[
        :, ["Calories", "StepTotal", "TotalIntensity", "AverageIntensity"]
    ]
    print(round(cols.corr()["Calories"], 4))


def plot_3_2():
    sleep_df = load_sleep()
    sleep_df = sleep_df.drop_duplicates(subset=["Id", "Date"])

    asleep: Series = sleep_df.loc[:, "TotalMinutesAsleep"]
    in_bed: Series = sleep_df.loc[:, "TotalTimeInBed"]
    records: Series = sleep_df.loc[:, "TotalSleepRecords"]
    gap: Series = in_bed - asleep

    print("Rows:", len(sleep_df), "Users:", sleep_df["Id"].nunique())
    print("Missing values:", sleep_df.isna().sum().sum())
    print("Asleep > in bed:", (asleep > in_bed).sum())
    print("Gap (min) min/median/max:", gap.min(), gap.median(), gap.max())
    print("Gap > 60 min:", (gap > 60).sum(), " Gap > 120 min:", (gap > 120).sum())
    print("Pearson r:", round(asleep.corr(in_bed), 4))

    print(gap.groupby(records).agg(["count", "mean", "max"]))

    sleep_df = sleep_df.assign(Gap=gap)
    print(sleep_df.sort_values(by="Gap", ascending=False).head(10))

    large: DataFrame = sleep_df.loc[sleep_df["Gap"] > 60]
    by_user = large["Id"].value_counts()
    print("Nights with gap > 60 per user head:")
    print(by_user.head(5))
    print("Top 2 users:", by_user.head(2).sum() / len(large))

    repeated: DataFrame = sleep_df.loc[sleep_df["TotalTimeInBed"] == 961]
    print("Nights with TotalTimeInBed == 961:")
    print(repeated)

    plot = (
        ggplot(sleep_df, aes(x="TotalTimeInBed", y="TotalMinutesAsleep"))
        + geom_abline(slope=1, intercept=0, linetype="dashed", color="red")
        + geom_point(alpha=0.5)
        + labs(
            title="Minutes Asleep vs Time in Bed",
            x="Time in bed (minutes)",
            y="Minutes asleep",
        )
        + theme_minimal()
    )

    plot.save("figures/asleep_vs_in_bed.png")


def plot_3_3(n_users=3, min_days=31, seed=1):
    hourly_df = build_hourly()

    users = select_users_by_days(hourly_df, min_days, n=n_users, seed=seed)
    print("Users:", users)

    selected: DataFrame = hourly_df.loc[hourly_df["Id"].isin(users)]
    selected = selected.assign(Hour=selected["Date"].dt.hour)

    mean_df = DataFrame(
        selected.groupby(["Id", "Hour"], as_index=False)["TotalIntensity"].mean()
    )
    print("Rows:", len(mean_df))

    for user in users:
        user_df: DataFrame = mean_df.loc[mean_df["Id"] == user]
        peak = user_df.loc[user_df["TotalIntensity"].idxmax()]

        print(
            f"{user}: peak hour {int(peak['Hour'])}, mean intensity {peak['TotalIntensity']:.2f}"
        )
        print(user_df.sort_values(by="TotalIntensity", ascending=False).head(3))

    y_max = float(mean_df["TotalIntensity"].to_numpy().max()) * 1.05

    for user in users:
        user_df = mean_df.loc[mean_df["Id"] == user]
        plot = (
            ggplot(user_df, aes(x="Hour", y="TotalIntensity"))
            + geom_col()
            + scale_x_continuous(breaks=list(range(0, 24)))
            + scale_y_continuous(limits=(0, y_max))
            + labs(
                title=f"Mean Intensity by Hour of Day: {user}",
                x="Hour of day (0-23)",
                y="Mean total intensity per hour",
            )
            + theme_minimal()
        )

        plot.save(f"figures/intensity_by_hour_{user}.png")


if __name__ == "__main__":
    # plot_3_1()
    # plot_3_2()
    plot_3_3()
