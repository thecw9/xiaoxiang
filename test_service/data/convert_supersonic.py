import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the xlsx file
supersonic_data = pd.read_excel("./supersonic_data_20221026.xlsx")

supersonic_data["tm"] = supersonic_data["Test_Time"]
# drop the Test_Time second is not 0
supersonic_data = supersonic_data[supersonic_data["tm"].dt.second == 0]

# time to isoformat
supersonic_data["tm"] = supersonic_data.apply(lambda x: x["tm"].isoformat(), axis=1)


print(supersonic_data.dtypes)

supersonic_data_channel_0 = supersonic_data[supersonic_data["channel"] == 0]
supersonic_data_channel_1 = supersonic_data[supersonic_data["channel"] == 1]
supersonic_data_channel_2 = supersonic_data[supersonic_data["channel"] == 2]
supersonic_data_channel_3 = supersonic_data[supersonic_data["channel"] == 3]
supersonic_data_channel_4 = supersonic_data[supersonic_data["channel"] == 4]
supersonic_data_channel_5 = supersonic_data[supersonic_data["channel"] == 5]
supersonic_data_channel_6 = supersonic_data[supersonic_data["channel"] == 6]
supersonic_data_channel_7 = supersonic_data[supersonic_data["channel"] == 7]

supersonic_channel_0_amp = supersonic_data_channel_0[["tm", "amp"]]
supersonic_channel_0_discharge = supersonic_data_channel_0[["tm", "discharge"]]
supersonic_channel_1_amp = supersonic_data_channel_1[["tm", "amp"]]
supersonic_channel_1_discharge = supersonic_data_channel_1[["tm", "discharge"]]
supersonic_channel_2_amp = supersonic_data_channel_2[["tm", "amp"]]
supersonic_channel_2_discharge = supersonic_data_channel_2[["tm", "discharge"]]
supersonic_channel_3_amp = supersonic_data_channel_3[["tm", "amp"]]
supersonic_channel_3_discharge = supersonic_data_channel_3[["tm", "discharge"]]
supersonic_channel_4_amp = supersonic_data_channel_4[["tm", "amp"]]
supersonic_channel_4_discharge = supersonic_data_channel_4[["tm", "discharge"]]
supersonic_channel_5_amp = supersonic_data_channel_5[["tm", "amp"]]
supersonic_channel_5_discharge = supersonic_data_channel_5[["tm", "discharge"]]
supersonic_channel_6_amp = supersonic_data_channel_6[["tm", "amp"]]
supersonic_channel_6_discharge = supersonic_data_channel_6[["tm", "discharge"]]
supersonic_channel_7_amp = supersonic_data_channel_7[["tm", "amp"]]
supersonic_channel_7_discharge = supersonic_data_channel_7[["tm", "discharge"]]

supersonic_channel_0_amp.columns = ["时间", "高压侧出线装置幅向超声局部放电幅值"]
supersonic_channel_0_discharge.columns = ["时间", "高压侧出线装置幅向超声局部放电次数"]
supersonic_channel_1_amp.columns = ["时间", "高压侧出线装置L弯超声局部放电幅值"]
supersonic_channel_1_discharge.columns = ["时间", "高压侧出线装置L弯超声局部放电次数"]
supersonic_channel_2_amp.columns = ["时间", "高压侧出线装置轴向超声局部放电幅值"]
supersonic_channel_2_discharge.columns = ["时间", "高压侧出线装置轴向超声局部放电次数"]
supersonic_channel_3_amp.columns = ["时间", "高压侧出线装置侧箱壁超声局部放电幅值"]
supersonic_channel_3_discharge.columns = [
    "时间",
    "高压侧出线装置侧箱壁超声局部放电次数",
]
supersonic_channel_4_amp.columns = ["时间", "高压套管末屏超声局部放电幅值"]
supersonic_channel_4_discharge.columns = ["时间", "高压套管末屏超声局部放电次数"]
supersonic_channel_5_amp.columns = ["时间", "冷却器对侧箱壁超声局部放电幅值"]
supersonic_channel_5_discharge.columns = ["时间", "冷却器对侧箱壁超声局部放电次数"]
supersonic_channel_6_amp.columns = ["时间", "铁芯夹件侧箱壁超声局部放电幅值"]
supersonic_channel_6_discharge.columns = ["时间", "铁芯夹件侧箱壁超声局部放电次数"]
supersonic_channel_7_amp.columns = ["时间", "冷却器侧箱壁超声局部放电幅值"]
supersonic_channel_7_discharge.columns = ["时间", "冷却器侧箱壁超声局部放电次数"]

print(supersonic_channel_0_amp)
print(supersonic_channel_0_discharge)

merged_data = pd.merge(
    supersonic_channel_0_amp, supersonic_channel_0_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_1_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_1_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_2_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_2_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_3_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_3_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_4_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_4_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_5_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_5_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_6_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_6_discharge, on="时间", how="outer"
)
merged_data = pd.merge(merged_data, supersonic_channel_7_amp, on="时间", how="outer")
merged_data = pd.merge(
    merged_data, supersonic_channel_7_discharge, on="时间", how="outer"
)

print(merged_data)
merged_data.to_csv("supersonic_data.csv", index=False)

# plot supersonic channel0 data

plt.figure(figsize=(10, 6))
plt.plot(
    merged_data["时间"],
    merged_data["高压侧出线装置幅向超声局部放电幅值"],
    label="高压侧出线装置幅向超声局部放电幅值",
)

plt.show()
