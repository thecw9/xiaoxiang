import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Read the data from the xlsx file
gis_data = pd.read_excel("./gis_data_20221026.xlsx")
# tm to iso format
gis_data["tm"] = gis_data.apply(lambda x: x["tm"].isoformat(), axis=1)

print(gis_data.dtypes)

gis_data_channel_1 = gis_data[gis_data["channel"] == 1]
gis_data_channel_2 = gis_data[gis_data["channel"] == 2]
gis_data_channel_3 = gis_data[gis_data["channel"] == 3]

gis_channel_1_maxdsch = gis_data_channel_1[["tm", "MaxDsch"]]
gis_channel_2_maxdsch = gis_data_channel_2[["tm", "MaxDsch"]]
gis_channel_3_maxdsch = gis_data_channel_3[["tm", "MaxDsch"]]
gis_channel_1_dschcnt = gis_data_channel_1[["tm", "DschCnt"]]
gis_channel_2_dschcnt = gis_data_channel_2[["tm", "DschCnt"]]
gis_channel_3_dschcnt = gis_data_channel_3[["tm", "DschCnt"]]
gis_channel_1_dschcnt = gis_data_channel_1[["tm", "DschCnt"]]

gis_channel_1_maxdsch.columns = ["时间", "夹件高频局部放电幅值"]
gis_channel_2_maxdsch.columns = ["时间", "铁芯高频局部放电幅值"]
gis_channel_3_maxdsch.columns = ["时间", "高压套管升高座高频局部放电幅值"]
gis_channel_1_dschcnt.columns = ["时间", "夹件高频局部放电次数"]
gis_channel_2_dschcnt.columns = ["时间", "铁芯高频局部放电次数"]
gis_channel_3_dschcnt.columns = ["时间", "高压套管升高座高频局部放电次数"]

merged_data = pd.merge(
    gis_channel_1_maxdsch, gis_channel_1_dschcnt, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, gis_channel_2_maxdsch, on="时间", how="outer")
merged_data = pd.merge(merged_data, gis_channel_2_dschcnt, on="时间", how="outer")
merged_data = pd.merge(merged_data, gis_channel_3_maxdsch, on="时间", how="outer")
merged_data = pd.merge(merged_data, gis_channel_3_dschcnt, on="时间", how="outer")

print(merged_data)
merged_data.to_csv("gis_data.csv", index=False)

# plot gis channel1 data
plt.figure(figsize=(10, 6))
plt.plot(
    merged_data["时间"][:50],
    merged_data["夹件高频局部放电幅值"][:50],
    label="夹件高频局部放电幅值",
)

plt.grid()
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.xticks(rotation=45)

plt.show()
