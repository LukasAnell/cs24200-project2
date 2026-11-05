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
