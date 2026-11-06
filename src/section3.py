import numpy as np
from pandas import DataFrame, Series
from plotnine import aes, geom_point, ggplot, labs, theme, theme_minimal

from process import build_hourly


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

    cols: DataFrame = hourly_df.loc[
        :, ["Calories", "StepTotal", "TotalIntensity", "AverageIntensity"]
    ]
    print(round(cols.corr()["Calories"], 4))


if __name__ == "__main__":
    plot_3_1()
