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


class OilModel:
    def __init__(
        self,
        path="/潇湘站/油色谱/1000kV潇江Ⅰ线高抗A相",
        device="1000kV潇江Ⅰ线高抗A相",
        alarm_report_path="alarm_report.pdf",
    ):
        self.path = path
        self.device = device
        self.alarm_report_path = alarm_report_path

        self.data = {}

    def generate_report(self):
        # tmp_file_dir = "/tmp/test"
        print("generate report")
        tmp_file_dir = f"/tmp/{uuid.uuid4()}"
        os.makedirs(tmp_file_dir, exist_ok=True)

        # convert to DataFrame
        df_list = []
        for key, value in self.data.items():
            # measure detai
            detail = fetch_measure_detail(key)
            key = detail["name"].split(".")[-1][:-8]

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

## 油色谱监测数据
{data_markdown}

## 故障诊断状态

{self.message}
        """

        save_markdown_to_pdf(text, f"{tmp_file_dir}/report.pdf")

        upload_file_to_minio(
            BUCKET_NAME, self.alarm_report_path, f"{tmp_file_dir}/report.pdf"
        )

    def predict(self):
        """
        Predict the value
        """
        self.status = 0
        self.message = ""

        data_limit = 30

        # c2h2 measurement
        c2h2_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_C2H2"
        )
        c2h2_key = c2h2_info["key"]
        c2h2_measurement_json = fetch_latest_history_data(c2h2_key, limit=data_limit)
        c2h2_measurement = c2h2_measurement_json[0]["value"]
        self.data[f"{c2h2_key}"] = c2h2_measurement_json

        # ch4 data
        ch4_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_CH4"
        )
        ch4_key = ch4_info["key"]
        ch4_measurement_json = fetch_latest_history_data(ch4_key, limit=data_limit)
        ch4_increments_4_hours = (
            ch4_measurement_json[0]["value"] - ch4_measurement_json[3]["value"]
        )
        self.data[f"{ch4_key}"] = ch4_measurement_json

        # h2 data
        h2_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_H2"
        )
        h2_key = h2_info["key"]
        h2_measurement_json = fetch_latest_history_data(h2_key, limit=data_limit)
        h2_measurement = h2_measurement_json[0]["value"]
        h2_increments_4_hours = (
            h2_measurement_json[0]["value"] - h2_measurement_json[3]["value"]
        )
        self.data[f"{h2_key}"] = h2_measurement_json

        # total hydrocarbon
        tothyd_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_总烃", exclude="增长&增量&告警"
        )
        tothyd_key = tothyd_info["key"]
        total_hydrocarbon_measurement_json = fetch_latest_history_data(
            tothyd_key, limit=data_limit
        )
        total_hydrocarbon_increments_4_hours = (
            total_hydrocarbon_measurement_json[0]["value"]
            - total_hydrocarbon_measurement_json[3]["value"]
        )
        self.data[f"{tothyd_key}"] = total_hydrocarbon_measurement_json

        # c2h4 data
        c2h4_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_C2H4"
        )
        c2h4_key = c2h4_info["key"]
        c2h4_measurement_json = fetch_latest_history_data(c2h4_key, limit=data_limit)
        c2h4_increments_4_hours = (
            c2h4_measurement_json[0]["value"] - c2h4_measurement_json[3]["value"]
        )
        self.data[f"{c2h4_key}"] = c2h4_measurement_json

        # c2h6 data
        c2h6_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_C2H6"
        )
        c2h6_key = c2h6_info["key"]
        c2h6_measurement_json = fetch_latest_history_data(c2h6_key, limit=data_limit)
        c2h6_increments_4_hours = (
            c2h6_measurement_json[0]["value"] - c2h6_measurement_json[3]["value"]
        )
        self.data[f"{c2h6_key}"] = c2h6_measurement_json

        # co data
        co_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_CO",
            exclude="第二套油色谱在线监测_CO2",
        )
        co_key = co_info["key"]
        co_measurement_json = fetch_latest_history_data(co_key, limit=data_limit)
        co_increments_1_day = (
            co_measurement_json[0]["value"] - co_measurement_json[23]["value"]
        )
        self.data[f"{co_key}"] = co_measurement_json

        # co2 data
        co2_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_CO2"
        )
        co2_key = co2_info["key"]
        co2_measurement_json = fetch_latest_history_data(co2_key, limit=data_limit)
        co2_increments_1_day = (
            co2_measurement_json[0]["value"] - co2_measurement_json[23]["value"]
        )
        self.data[f"{co2_key}"] = co2_measurement_json

        # 乙炔测量量超过0.1，存在潜在风险。
        if c2h2_measurement >= 0.1 and h2_measurement >= 1:
            self.message += f"<b>乙炔测量量</b>（测点：{c2h2_key}，实时值：{c2h2_measurement}）超过0.1，<b>氢气测量量</b>（测点：{h2_key}，实时值：{h2_measurement}）超过1。"
            self.status += 1
        elif (
            c2h2_measurement > 0.02 and c2h2_measurement <= 0.1 and h2_measurement >= 1
        ):
            self.message += f"<b>乙炔测量量</b>（测点：{c2h2_key}，实时值：{c2h2_measurement}）从无到有，氢气测量量（测点：{h2_key}，实时值：{h2_measurement}）超过1。"
            self.status += 1
        else:
            self.message += f"<b>乙炔测量量</b>（测点：{c2h2_key}，实时值：{c2h2_measurement}）正常，<b>氢气测量量</b>（测点：{h2_key}，实时值：{h2_measurement}）正常。"
            self.status = 0
            return {"status": self.status, "message": self.message, "data": ""}

        # 甲烷测量量增量超过乙烯、乙烷测量量增量，提2级管控。
        if (
            ch4_increments_4_hours > c2h4_increments_4_hours
            and ch4_increments_4_hours > c2h6_increments_4_hours
        ):
            self.message += f"<b>甲烷4小时增量</b>（测点：{ch4_key}，实时值：{round(ch4_increments_4_hours,4)}）超过乙烯、乙烷4小时增量（测点：{c2h4_key}，实时值：{round(c2h4_increments_4_hours,4)}）、（测点：{c2h6_key}，实时值：{round(c2h6_increments_4_hours,4)}），提2级管控。"
            self.status = 2
            self.generate_report()
            return {
                "status": self.status,
                "message": self.message,
                "data": self.data,
            }

        # 出现明显增长，出现局部放电
        if (
            ch4_increments_4_hours > 0.1
            or c2h4_increments_4_hours > 0.1
            or c2h6_increments_4_hours > 0.1
        ):
            self.message += f"甲烷、乙烯、乙烷测量量增量{ch4_increments_4_hours}、{c2h4_increments_4_hours}、{c2h6_increments_4_hours}超过0.1，出现局部放电。"
            self.status = 2
            # 一氧化碳增量超过100 或者 二氧化碳增量超过200，出现局部放电，涉及固体绝缘材料，故障点可能位于线圈，引线支撑件等部件。
            if co_increments_1_day > 100000 or co2_increments_1_day > 200000:
                self.message += f"一氧化碳、二氧化碳增量{co_increments_1_day}、{co2_increments_1_day}超过200，出现局部放电，涉及固体绝缘材料，故障点可能位于线圈，引线支撑件等部件。"
                self.status = 3
                self.generate_report()
                return {
                    "status": self.status,
                    "message": self.message,
                    "data": self.data,
                }

        # 无明显增长，跟踪监测，取油分析。
        if (
            ch4_increments_4_hours < 0.1
            and c2h4_increments_4_hours < 0.1
            and c2h6_increments_4_hours < 0.1
        ):
            self.message += (
                "甲烷、乙烯、乙烷测量量增量均小于0.1，无明显增长，跟踪监测，取油分析。"
            )
            self.status = 1
            self.generate_report()
            return {
                "status": self.status,
                "message": self.message,
                "data": self.data,
            }

        return {"status": 0, "message": "无风险", "data": ""}


if __name__ == "__main__":
    model = OilModel()
    result = model.predict()
    model.generate_report()
    print(result)
