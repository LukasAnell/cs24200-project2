from pandas import DataFrame, Series
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

from process import load_daily_activity


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


if __name__ == "__main__":
    plot_1c()
