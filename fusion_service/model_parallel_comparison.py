import argparse
import math
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


def check_increasing_or_decreasing(data: np.ndarray) -> int:
    """
    Check if the data is increasing or decreasing
    """
    # check if the data is increasing
    if np.all(np.diff(data) > 0):
        return 1
    # check if the data is decreasing
    elif np.all(np.diff(data) < 0):
        return -1
    else:
        return 0


class ParallelComparisonModel:
    def __init__(
        self,
        path="/潇湘站/横向趋势判别/1000kV潇江Ⅰ线高抗",
        device="1000kV潇江Ⅰ线高抗",
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

        # A相 c2h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&A相&第二套油色谱在线监测_C2H2"
        )
        c2h2_phase_a_measurement_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = c2h2_phase_a_measurement_json

        # B相 c2h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&B相&第二套油色谱在线监测_C2H2"
        )
        c2h2_phase_b_measurement_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = c2h2_phase_b_measurement_json

        # C相 c2h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&C相&第二套油色谱在线监测_C2H2"
        )
        c2h2_phase_c_measurement_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = c2h2_phase_c_measurement_json

        # A相 h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&A相&第二套油色谱在线监测_H2"
        )
        h2_phase_a_measurement_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = h2_phase_a_measurement_json

        # B相 h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&B相&第二套油色谱在线监测_H2"
        )
        h2_phase_b_measurement_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = h2_phase_b_measurement_json

        # C相 h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&C相&第二套油色谱在线监测_H2"
        )
        h2_phase_c_measurement_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = h2_phase_c_measurement_json

        # 2. 判断是否需要预警
        c2h2_phase_a_measurements = pd.DataFrame(c2h2_phase_a_measurement_json[:4])
        c2h2_phase_a_measurements_np = c2h2_phase_a_measurements["value"].to_numpy()
        c2h2_phase_b_measurements = pd.DataFrame(c2h2_phase_b_measurement_json[:4])
        c2h2_phase_b_measurements_np = c2h2_phase_b_measurements["value"].to_numpy()
        c2h2_phase_c_measurements = pd.DataFrame(c2h2_phase_c_measurement_json[:4])
        c2h2_phase_c_measurements_np = c2h2_phase_c_measurements["value"].to_numpy()

        c2h2_data = np.vstack(
            [
                c2h2_phase_a_measurements_np,
                c2h2_phase_b_measurements_np,
                c2h2_phase_c_measurements_np,
            ]
        )

        max_value = np.max(c2h2_data, axis=0)
        min_value = np.min(c2h2_data, axis=0)
        diff_value = max_value - min_value
        mean_value = np.mean(diff_value[:-1])
        if np.abs(diff_value[-1] - mean_value) / mean_value > 0.3:
            print(np.abs(diff_value[-1] - mean_value) / mean_value)
            self.status += 1
            self.message += "三相乙炔浓度差异过大"

        # 判断是否不是均上升或者均下降
        if_c2h2_phase_a_increasing = check_increasing_or_decreasing(
            c2h2_phase_a_measurements_np
        )
        if_c2h2_phase_b_increasing = check_increasing_or_decreasing(
            c2h2_phase_b_measurements_np
        )
        if_c2h2_phase_c_increasing = check_increasing_or_decreasing(
            c2h2_phase_c_measurements_np
        )

        increasing_list = np.array(
            [
                if_c2h2_phase_a_increasing,
                if_c2h2_phase_b_increasing,
                if_c2h2_phase_c_increasing,
            ]
        )

        if (
            not np.all(increasing_list == 1)
            and not np.all(increasing_list == -1)
            and np.all(increasing_list != 0)
        ):
            self.status += 1
            self.message += "三相乙炔浓度变化趋势不一致"

        h2_phase_a_measurements = pd.DataFrame(h2_phase_a_measurement_json[:3])
        h2_phase_a_measurements_np = h2_phase_a_measurements["value"].to_numpy()
        h2_phase_b_measurements = pd.DataFrame(h2_phase_b_measurement_json[:3])
        h2_phase_b_measurements_np = h2_phase_b_measurements["value"].to_numpy()
        h2_phase_c_measurements = pd.DataFrame(h2_phase_c_measurement_json[:3])
        h2_phase_c_measurements_np = h2_phase_c_measurements["value"].to_numpy()

        h2_data = np.vstack(
            [
                h2_phase_a_measurements_np,
                h2_phase_b_measurements_np,
                h2_phase_c_measurements_np,
            ]
        )

        max_value = np.max(h2_data, axis=0)
        min_value = np.min(h2_data, axis=0)
        diff_value = max_value - min_value
        if np.abs(diff_value[-1] / np.mean(diff_value[:-1]) - 1) > 0.3:
            self.status += 1
            self.message += "三相氢气浓度差异过大"

        # 判断是否不是均上升或者均下降
        if_h2_phase_a_increasing = check_increasing_or_decreasing(
            h2_phase_a_measurements_np
        )
        if_h2_phase_b_increasing = check_increasing_or_decreasing(
            h2_phase_b_measurements_np
        )
        if_h2_phase_c_increasing = check_increasing_or_decreasing(
            h2_phase_c_measurements_np
        )

        increasing_list = np.array(
            [
                if_h2_phase_a_increasing,
                if_h2_phase_b_increasing,
                if_h2_phase_c_increasing,
            ]
        )

        if (
            not np.all(increasing_list == 1)
            and not np.all(increasing_list == -1)
            and np.all(increasing_list != 0)
        ):
            self.status += 1
            self.message += "三相氢气浓度变化趋势不一致"

        # 3. 生成报告
        if self.status > 0:
            self.generate_alarm_report()

        # 4. 返回结果
        if self.status == 0:
            self.message = "数据正常"
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
    model = ParallelComparisonModel()
    result = model.predict()
    model.generate_alarm_report()
    print(result)
    print("Done")
