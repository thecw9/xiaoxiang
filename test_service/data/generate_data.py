import pandas as pd
from datetime import datetime

# read gis data and supersonic data
gis_data = pd.read_csv("gis_data.csv")
supersonic_data = pd.read_csv("supersonic_data.csv")
oil_chromatograph_data = pd.read_csv("./oil_chro_data.csv")

# merge the two dataframes
data = pd.merge(gis_data, supersonic_data, on="时间", how="outer")
data = pd.merge(data, oil_chromatograph_data, on="时间", how="outer")
print(data)

data["时间"] = pd.to_datetime(data["时间"])

# convert time year to 2099
data["时间"] = data["时间"].apply(lambda x: x.replace(year=2099))

# filter data <= 2099-10-26 01:00:00
filtered_data = data[data["时间"] <= pd.Timestamp("2099-10-26 01:00:00")]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-01:00:00.csv", index=False)

# filter data <= 2099-10-26 01:45:00
filtered_data = data[data["时间"] <= pd.Timestamp("2099-10-26 01:45:00")]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-01:45:00.csv", index=False)

# filter data <= 2099-10-26 03:15:00
filtered_data = data[data["时间"] <= pd.Timestamp("2099-10-26 03:15:00")]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-03:15:00.csv", index=False)

# filter data <= 2099-10-26 03:30:00
filtered_data = data[data["时间"] <= pd.Timestamp("2099-10-26 03:30:00")]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-03:30:00.csv", index=False)

# filter data <= 2099-10-26 03:35:00
filtered_data = data[data["时间"] <= pd.Timestamp("2099-10-26 03:35:00")]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-03:35:00.csv", index=False)


# filter data <= 2099-10-26 07:05:00
filtered_data = data[data["时间"] <= pd.Timestamp("2099-10-26 07:05:00")]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-07:05:00.csv", index=False)

# filter data <= 2099-10-26 11:00:00 and >= 2099-10-26 09:00:00
filtered_data = data[
    (data["时间"] <= pd.Timestamp("2099-10-26 11:00:00"))
    & (data["时间"] >= pd.Timestamp("2099-10-26 01:00:00"))
]
# save the data
filtered_data.to_csv("荆潇Ⅰ线高抗C相故障-11:00:00.csv", index=False)
