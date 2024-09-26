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


# def is_stepwise_increase(data: np.ndarray, threshold: float = 0.01) -> bool:
#     """
#     检查数据是否呈现逐步增加的趋势
#     """
#     n = data.shape[0]
#     # 检查第一列是否逐步增加
#     for i in range(1, n):
#         if data[i, 0] - data[i - 1, 0] < threshold:
#             return False
#
#     # 检查每一行的值是否都大于这一行第一个值
#     for i in range(n):
#         if not np.all(data[i, 1:] >= data[i, 0]):
#             return False
#
#     # 检查每一行的值是否都小于下一行第一个值
#     for i in range(n - 1):
#         if not np.all(data[i, :] <= data[i + 1, 0]):
#             return False
#
#     return True


def is_stepwise_increase(data: np.ndarray, threshold: float = 0.01) -> bool:
    """
    检查数据是否呈现逐步增加的趋势
    """
    row_means = np.mean(data, axis=1)
    n = row_means.shape[0]
    # 检查平均值是否逐步增加
    for i in range(1, n):
        if row_means[i] - row_means[i - 1] < threshold:
            return False
    return True


class C2h2StepwiseModel:
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
        STEP_LENGTH = 3 * 24
        STEP_HIGH_THRESHOLD = 0.01
        data_limit = STEP_LENGTH * 3

        # c2h2 data
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_C2H2"
        )
        c2h2_measurement_json = fetch_latest_history_data(info["key"], limit=data_limit)
        self.data[f"{info['key']}"] = c2h2_measurement_json

        if len(c2h2_measurement_json) < data_limit:
            self.status = -1
            self.message = "乙炔浓度数据不足，无法进行预警。"
            return {
                "status": self.status,
                "message": self.message,
            }

        # 2. 判断是否需要预警
        c2h2_measurements = pd.DataFrame(c2h2_measurement_json)
        # to numpy
        c2h2_measurements_np = c2h2_measurements["value"].to_numpy()
        c2h2_measurements_np = c2h2_measurements_np.reshape(-1, STEP_LENGTH)
        print(c2h2_measurements_np)

        if is_stepwise_increase(c2h2_measurements_np, STEP_HIGH_THRESHOLD):
            self.status = 1
            self.message = "乙炔浓度逐步增加，请注意安全。"
        else:
            self.status = 0
            self.message = "乙炔浓度未发现逐步增加趋势。"

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

## 乙炔监测数据
{data_markdown}

## 诊断信息

{self.message}
        """

        save_markdown_to_pdf(text, f"{tmp_file_dir}/report.pdf")

        upload_file_to_minio(
            BUCKET_NAME, self.alarm_report_path, f"{tmp_file_dir}/report.pdf"
        )


if __name__ == "__main__":
    model = C2h2StepwiseModel()
    result = model.predict()
    model.generate_alarm_report()
    print(result)
    print("Done")
