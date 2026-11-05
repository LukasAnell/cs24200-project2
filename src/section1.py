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

dailyActivity_df = load_daily_activity()

counts = dailyActivity_df["Id"].value_counts()
print("Rows per Id:", counts)

qualifying_Ids = counts.loc[counts == 31].sort_index()
print("Qualifying Ids:", qualifying_Ids)

random_Ids = qualifying_Ids.sample(n=5, random_state=1)
print("5 Random Ids:", random_Ids)

filtered_dailyActivity_df = dailyActivity_df.loc[
    dailyActivity_df["Id"].isin(random_Ids.index)
]
print("Shape:", filtered_dailyActivity_df.shape)
print("df:", filtered_dailyActivity_df.head())

print("nunique:", filtered_dailyActivity_df["Id"].nunique())

print(
    "min, max, mean:",
    filtered_dailyActivity_df.groupby("Id")["TotalSteps"].agg(["min", "max", "mean"]),
)

print(
    "zero step days:",
    (filtered_dailyActivity_df["TotalSteps"] == 0)
    .groupby(filtered_dailyActivity_df["Id"])
    .sum(),
)

filtered_dailyActivity_df["Id"] = filtered_dailyActivity_df["Id"].astype("category")

plot = (
    ggplot(
        filtered_dailyActivity_df, aes(x="Date", y="TotalSteps", color="Id", group="Id")
    )
    + geom_line(size=1)
    + scale_x_date(date_breaks="1 week", date_labels="%b %d")
    + labs(title="Total Steps Over Time by ID", x="Date", y="Total Steps", color="ID")
    + theme_minimal()
    + theme(axis_text_x=element_text(rotation=45, hjust=1), figure_size=(10, 6))
)

plot.save("total_steps_by_id.png")
