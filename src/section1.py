from pandas import DataFrame
from plotnine import (
    aes,
    element_text,
    geom_line,
    ggplot,
    labs,
    scale_x_date,
    theme,
    theme_minimal,
)

from process import load_daily_activity, load_sleep


def select_users(df: DataFrame, min_days, n=5, seed=1) -> list:
    counts = df["Id"].value_counts()
    qualifying_Ids = counts.loc[counts >= min_days].sort_index()
    return qualifying_Ids.sample(n=n, random_state=seed).index.to_list()


def filter_users(df: DataFrame, ids) -> DataFrame:
    filtered_df: DataFrame = df.loc[df["Id"].isin(ids)]
    filtered_df["Id"] = filtered_df["Id"].astype("category")
    return filtered_df


def plot_user_lines(df: DataFrame, y: str, ylabel: str, title: str, filename: str):
    plot = (
        ggplot(
            df,
            aes(x="Date", y=y, color="Id", group="Id"),
        )
        + geom_line(size=1)
        + scale_x_date(date_breaks="1 week", date_labels="%b %d")
        + labs(title=title, x="Date", y=ylabel, color="ID")
        + theme_minimal()
        + theme(axis_text_x=element_text(rotation=45, hjust=1), figure_size=(10, 6))
    )

    plot.save(filename)


def plot_1c():
    dailyActivity_df = load_daily_activity()

    random_users = select_users(dailyActivity_df, 31)

    filtered_dailyActivity_df = filter_users(dailyActivity_df, random_users)

    plot_user_lines(
        filtered_dailyActivity_df,
        "TotalSteps",
        "Total Steps",
        "Total Steps Over Time by ID",
        "total_steps_by_id.png",
    )


def plot_1b():
    sleepDay_df = load_sleep()
    sleepDay_df = sleepDay_df.drop_duplicates(subset=["Id", "Date"])

    random_users = select_users(sleepDay_df, 25)
    print(random_users)

    filtered_sleepDay_df = filter_users(sleepDay_df, random_users)

    print(
        "min/max/mean:",
        filtered_sleepDay_df.groupby(by="Id", as_index=False)["TotalMinutesAsleep"].agg(
            ["min", "max", "mean"]
        ),
    )

    total_days = (sleepDay_df["Date"].max() - sleepDay_df["Date"].min()).days + 1
    present = filtered_sleepDay_df.groupby("Id")["Date"].nunique()
    missing = total_days - present
    print("Missing days:", missing)

    plot_user_lines(
        filtered_sleepDay_df,
        "TotalMinutesAsleep",
        "Minutes Asleep",
        "Minutes Asleep Over Time by ID",
        "minutes_asleep_by_id.png",
    )


if __name__ == "__main__":
    # plot_1c()
    plot_1b()
