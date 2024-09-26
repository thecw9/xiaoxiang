import argparse
import uuid
from config import BUCKET_NAME
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.numerictypes import ScalarType
from datetime import datetime, timedelta
import os
from typing import Optional
from minio import Minio
from pprint import pprint
import markdown
from weasyprint import HTML, CSS

from utils import (
    fetch_measure_detail,
    fetch_measure_info_by_keyword,
    save_markdown_to_pdf,
    upload_file_to_minio,
    fetch_latest_history_data,
)


class C2h2H2Model:
    def __init__(
        self,
        path="/潇湘站/乙炔-氢气/1000kV潇江Ⅰ线高抗A相",
        device="1000kV潇江Ⅰ线高抗A相",
        alarm_report_path="alarm_report.pdf",
    ):
        self.path = path
        self.device = device
        self.alarm_report_path = alarm_report_path

        self.data = {}

    def predict(self) -> dict:
        self.message = ""
        self.status = 0

        # 1. 获取最新的历史数据
        data_limit = 30

        # c2h2 data
        c2h2_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_C2H2"
        )
        c2h2_key = c2h2_info["key"]
        c2h2_measurement_json = fetch_latest_history_data(
            c2h2_info["key"], limit=data_limit
        )
        self.data[f"{c2h2_info['key']}"] = c2h2_measurement_json

        # h2 data
        h2_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_H2"
        )
        h2_key = h2_info["key"]
        h2_measurement_json = fetch_latest_history_data(h2_key, limit=data_limit)
        self.data[f"{h2_key}"] = h2_measurement_json

        # 2. 判断是否需要预警
        c2h2_increments_2_hours = (
            c2h2_measurement_json[0]["value"] - c2h2_measurement_json[2]["value"]
        )
        c2h2_increments_4_hours = (
            c2h2_measurement_json[0]["value"] - c2h2_measurement_json[4]["value"]
        )
        c2h2_increments_6_hours = (
            c2h2_measurement_json[0]["value"] - c2h2_measurement_json[6]["value"]
        )
        h2_increments_2_hours = (
            h2_measurement_json[0]["value"] - h2_measurement_json[2]["value"]
        )
        h2_increments_4_hours = (
            h2_measurement_json[0]["value"] - h2_measurement_json[4]["value"]
        )
        h2_increments_6_hours = (
            h2_measurement_json[0]["value"] - h2_measurement_json[6]["value"]
        )
        if c2h2_increments_2_hours >= 0.01 and h2_increments_2_hours > 0.01:
            self.status += 1
            self.message += f"<b>乙炔2小时增量</b>（测点：{c2h2_key}，实时值：{c2h2_increments_2_hours}）超过0.01，<b>氢气2小时增量</b>（测点：{h2_key}，实时值：{h2_increments_2_hours}）超过0.01，请注意！\n"
        if c2h2_increments_4_hours >= 0.01 and h2_increments_4_hours > 0.01:
            self.status += 1
            self.message += f"<b>乙炔4小时增量</b>（测点：{c2h2_key}，实时值：{c2h2_increments_4_hours}）超过0.01，<b>氢气4小时增量</b>（测点：{h2_key}，实时值：{h2_increments_4_hours}）超过0.01，请注意！\n"
        if c2h2_increments_6_hours >= 0.01 and h2_increments_6_hours > 0.01:
            self.status += 1
            self.message += f"<b>乙炔6小时增量</b>（测点：{c2h2_key}，实时值：{c2h2_increments_6_hours}）超过0.01，<b>氢气6小时增量</b>（测点：{h2_key}，实时值：{h2_increments_6_hours}）超过0.01，请注意！\n"

        if self.status == 0:
            self.message = "乙炔和氢气浓度正常"
        else:
            self.status = 3
            self.message = "<b>乙炔和氢气出现同步增长。</b>\n" + self.message

        # 3. 生成报告
        if self.status > 0:
            self.generate_alarm_report()

        # 4. 返回结果
        return {
            "status": self.status,
            "message": self.message,
        }

    def generate_alarm_report(self):
        # tmp_file_dir = "/tmp/test"
        print("generate report")
        tmp_file_dir = f"/tmp/{uuid.uuid4()}"
        os.makedirs(tmp_file_dir, exist_ok=True)

        # convert to DataFrame
        df_list = []
        for key, value in self.data.items():
            # measure detai
            detail = fetch_measure_detail(key)
            key = detail["name"].split(".")[-1]

            df = pd.DataFrame(value)
            df = df[["time", "value"]]
            # save fresh_time only to minute
            df["time"] = df["time"].apply(lambda x: x[: x.rfind(":")])
            df.columns = ["时间", key]
            df.set_index("时间", inplace=True)
            # remove duplicated time row
            df = df[~df.index.duplicated(keep="first")]

            df_list.append(df)

        # merge all data
        self.data_df = pd.concat(df_list, axis=1)

        data_markdown = self.data_df.to_markdown()

        text = f"""
# {self.path}诊断报告

## 乙炔和氢气监测数据
{data_markdown}

## 诊断信息

{self.message}
        """

        save_markdown_to_pdf(text, f"{tmp_file_dir}/report.pdf")

        upload_file_to_minio(
            BUCKET_NAME, self.alarm_report_path, f"{tmp_file_dir}/report.pdf"
        )


if __name__ == "__main__":
    model = C2h2H2Model()
    result = model.predict()
    model.generate_alarm_report()
    print(result)
    print("Done")
