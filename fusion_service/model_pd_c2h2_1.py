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


class PdC2h2Model:
    def __init__(
        self,
        path="/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗A相",
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

        # 乙炔数据
        info = fetch_measure_info_by_keyword(include=f"{self.device}&乙炔测量量")
        c2h2_measurement_json = fetch_latest_history_data(info["key"], limit=data_limit)
        self.data[f"{info['key']}"] = c2h2_measurement_json

        # 高压套管升高座高频局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压套管升高座高频局部放电幅值"
        )
        high_voltage_bushing_elevation_seat_high_frequency_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_bushing_elevation_seat_high_frequency_pd_amplitude_json
        )

        # 高压套管升高座高频局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压套管升高座高频局部放电次数"
        )
        high_voltage_bushing_elevation_seat_high_frequency_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_bushing_elevation_seat_high_frequency_pd_count_json
        )

        # 高压侧出线装置幅向超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置幅向超声局部放电幅值"
        )
        high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude_json
        )

        # 高压侧出线装置幅向超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置幅向超声局部放电次数"
        )
        high_voltage_side_outlet_device_radial_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_radial_ultrasonic_pd_count_json
        )

        # 高压侧出线装置L弯超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置L弯超声局部放电幅值"
        )
        high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude_json
        )

        # 高压侧出线装置L弯超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置L弯超声局部放电次数"
        )
        high_voltage_side_outlet_device_l_bend_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_l_bend_ultrasonic_pd_count_json
        )

        # 高压侧出线装置轴向超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置轴向超声局部放电幅值"
        )
        high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude_json
        )

        # 高压侧出线装置轴向超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置轴向超声局部放电次数"
        )
        high_voltage_side_outlet_device_axial_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_axial_ultrasonic_pd_count_json
        )

        # 高压侧出线装置箱壁超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置&箱壁超声局部放电幅值"
        )
        high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude_json
        )

        # 高压侧出线装置箱壁超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压侧出线装置&箱壁超声局部放电次数"
        )
        high_voltage_side_outlet_device_box_wall_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_side_outlet_device_box_wall_ultrasonic_pd_count_json
        )

        # 高压套管末屏超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压套管末屏超声局部放电幅值"
        )
        high_voltage_bushing_end_screen_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_bushing_end_screen_ultrasonic_pd_amplitude_json
        )

        # 高压套管末屏超声局部放电放电次数
        print(self.device)
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&高压套管末屏超声局部放电&次数"
        )
        high_voltage_bushing_end_screen_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            high_voltage_bushing_end_screen_ultrasonic_pd_count_json
        )

        # 冷却器对侧箱壁超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&冷却器对侧箱壁超声局部放电幅值"
        )
        cooler_opposite_side_box_wall_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            cooler_opposite_side_box_wall_ultrasonic_pd_amplitude_json
        )

        # 冷却器对侧箱壁超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&冷却器对侧箱壁超声局部放电次数"
        )
        cooler_opposite_side_box_wall_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            cooler_opposite_side_box_wall_ultrasonic_pd_count_json
        )

        # 铁芯夹件侧箱壁超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&铁芯夹件侧箱壁超声局部放电幅值"
        )
        iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude_json
        )

        # 铁芯夹件侧箱壁超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&铁芯夹件侧箱壁超声局部放电次数"
        )
        iron_core_clamp_side_box_wall_ultrasonic_pd_count_json = (
            fetch_latest_history_data(info["key"], limit=data_limit)
        )
        self.data[f"{info['key']}"] = (
            iron_core_clamp_side_box_wall_ultrasonic_pd_count_json
        )

        # 冷却器侧箱壁超声局部放电幅值
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&冷却器侧箱壁超声局部放电幅值"
        )
        cooler_side_box_wall_ultrasonic_pd_amplitude_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = cooler_side_box_wall_ultrasonic_pd_amplitude_json

        # 冷却器侧箱壁超声局部放电次数
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&冷却器侧箱壁超声局部放电次数"
        )
        cooler_side_box_wall_ultrasonic_pd_count_json = fetch_latest_history_data(
            info["key"], limit=data_limit
        )
        self.data[f"{info['key']}"] = cooler_side_box_wall_ultrasonic_pd_count_json

        # 2. 判断是否需要预警
        c2h2_increments_4_hours = (
            c2h2_measurement_json[0]["value"] - c2h2_measurement_json[3]["value"]
        )
        C2H2_THRESHOLD = 0.1
        HIGH_FREQUENCY_PD_AMPLITUDE_THRESHOLD = 0.1
        HIGH_FREQUENCY_PD_COUNT_THRESHOLD = 1000
        ULTRASONIC_PD_AMPLITUDE_THRESHOLD = 1000
        ULTRASONIC_PD_COUNT_THRESHOLD = 0
        if c2h2_increments_4_hours > C2H2_THRESHOLD:
            self.status = 0
            self.message += f"乙炔浓度4小时增长{c2h2_increments_4_hours}。"

            # 高压套管升高座高频局部放电幅值
            high_voltage_bushing_elevation_seat_high_frequency_pd_amplitude = (
                high_voltage_bushing_elevation_seat_high_frequency_pd_amplitude_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_bushing_elevation_seat_high_frequency_pd_amplitude
                > HIGH_FREQUENCY_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压套管升高座高频局部放电幅值为{high_voltage_bushing_elevation_seat_high_frequency_pd_amplitude}，请注意！"

            # 高压套管升高座高频局部放电次数
            high_voltage_bushing_elevation_seat_high_frequency_pd_count = (
                high_voltage_bushing_elevation_seat_high_frequency_pd_count_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_bushing_elevation_seat_high_frequency_pd_count
                > HIGH_FREQUENCY_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压套管升高座高频局部放电次数为{high_voltage_bushing_elevation_seat_high_frequency_pd_count}，请注意！"

            # 高压侧出线装置幅向超声局部放电幅值
            high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude = (
                high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置幅向超声局部放电幅值为{high_voltage_side_outlet_device_radial_ultrasonic_pd_amplitude}，请注意！"

            # 高压侧出线装置幅向超声局部放电次数
            high_voltage_side_outlet_device_radial_ultrasonic_pd_count = (
                high_voltage_side_outlet_device_radial_ultrasonic_pd_count_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_radial_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置幅向超声局部放电次数为{high_voltage_side_outlet_device_radial_ultrasonic_pd_count}，请注意！"

            # 高压侧出线装置L弯超声局部放电幅值
            high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude = (
                high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置L弯超声局部放电幅值为{high_voltage_side_outlet_device_l_bend_ultrasonic_pd_amplitude}，请注意！"

            # 高压侧出线装置L弯超声局部放电次数
            high_voltage_side_outlet_device_l_bend_ultrasonic_pd_count = (
                high_voltage_side_outlet_device_l_bend_ultrasonic_pd_count_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_l_bend_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置L弯超声局部放电次数为{high_voltage_side_outlet_device_l_bend_ultrasonic_pd_count}，请注意！"

            # 高压侧出线装置轴向超声局部放电幅值
            high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude = (
                high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置轴向超声局部放电幅值为{high_voltage_side_outlet_device_axial_ultrasonic_pd_amplitude}，请注意！"

            # 高压侧出线装置轴向超声局部放电次数
            high_voltage_side_outlet_device_axial_ultrasonic_pd_count = (
                high_voltage_side_outlet_device_axial_ultrasonic_pd_count_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_axial_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置轴向超声局部放电次数为{high_voltage_side_outlet_device_axial_ultrasonic_pd_count}，请注意！"

            # 高压侧出线装置箱壁超声局部放电幅值
            high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude = (
                high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude_json[
                    0
                ]["value"]
            )
            if (
                high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置箱壁超声局部放电幅值为{high_voltage_side_outlet_device_box_wall_ultrasonic_pd_amplitude}，请注意！"

            # 高压侧出线装置箱壁超声局部放电次数
            high_voltage_side_outlet_device_box_wall_ultrasonic_pd_count = (
                high_voltage_side_outlet_device_box_wall_ultrasonic_pd_count_json[0][
                    "value"
                ]
            )
            if (
                high_voltage_side_outlet_device_box_wall_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压侧出线装置箱壁超声局部放电次数为{high_voltage_side_outlet_device_box_wall_ultrasonic_pd_count}，请注意！"

            # 高压套管末屏超声局部放电幅值
            high_voltage_bushing_end_screen_ultrasonic_pd_amplitude = (
                high_voltage_bushing_end_screen_ultrasonic_pd_amplitude_json[0]["value"]
            )
            if (
                high_voltage_bushing_end_screen_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or high_voltage_bushing_end_screen_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压套管末屏超声局部放电幅值为{high_voltage_bushing_end_screen_ultrasonic_pd_amplitude}，请注意！"

            # 高压套管末屏超声局部放电放电次数
            high_voltage_bushing_end_screen_ultrasonic_pd_count = (
                high_voltage_bushing_end_screen_ultrasonic_pd_count_json[0]["value"]
            )
            if (
                high_voltage_bushing_end_screen_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"高压套管末屏超声局部放电放电次数为{high_voltage_bushing_end_screen_ultrasonic_pd_count}，请注意！"

            # 冷却器对侧箱壁超声局部放电幅值
            cooler_opposite_side_box_wall_ultrasonic_pd_amplitude = (
                cooler_opposite_side_box_wall_ultrasonic_pd_amplitude_json[0]["value"]
            )
            if (
                cooler_opposite_side_box_wall_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or cooler_opposite_side_box_wall_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"冷却器对侧箱壁超声局部放电幅值为{cooler_opposite_side_box_wall_ultrasonic_pd_amplitude}，请注意！"

            # 冷却器对侧箱壁超声局部放电次数
            cooler_opposite_side_box_wall_ultrasonic_pd_count = (
                cooler_opposite_side_box_wall_ultrasonic_pd_count_json[0]["value"]
            )
            if (
                cooler_opposite_side_box_wall_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"冷却器对侧箱壁超声局部放电次数为{cooler_opposite_side_box_wall_ultrasonic_pd_count}，请注意！"

            # 铁芯夹件侧箱壁超声局部放电幅值
            iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude = (
                iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude_json[0]["value"]
            )
            if (
                iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"铁芯夹件侧箱壁超声局部放电幅值为{iron_core_clamp_side_box_wall_ultrasonic_pd_amplitude}，请注意！"

            # 铁芯夹件侧箱壁超声局部放电次数
            iron_core_clamp_side_box_wall_ultrasonic_pd_count = (
                iron_core_clamp_side_box_wall_ultrasonic_pd_count_json[0]["value"]
            )
            if (
                iron_core_clamp_side_box_wall_ultrasonic_pd_count
                > ULTRASONIC_PD_COUNT_THRESHOLD
            ):
                self.status += 1
                self.message += f"铁芯夹件侧箱壁超声局部放电次数为{iron_core_clamp_side_box_wall_ultrasonic_pd_count}，请注意！"

            # 冷却器侧箱壁超声局部放电幅值
            cooler_side_box_wall_ultrasonic_pd_amplitude = (
                cooler_side_box_wall_ultrasonic_pd_amplitude_json[0]["value"]
            )
            if (
                cooler_side_box_wall_ultrasonic_pd_amplitude
                > ULTRASONIC_PD_AMPLITUDE_THRESHOLD
                or cooler_side_box_wall_ultrasonic_pd_amplitude
                < -ULTRASONIC_PD_AMPLITUDE_THRESHOLD
            ):
                self.status += 1
                self.message += f"冷却器侧箱壁超声局部放电幅值为{cooler_side_box_wall_ultrasonic_pd_amplitude}，请注意！"

            # 冷却器侧箱壁超声局部放电次数
            cooler_side_box_wall_ultrasonic_pd_count = (
                cooler_side_box_wall_ultrasonic_pd_count_json[0]["value"]
            )
            if cooler_side_box_wall_ultrasonic_pd_count > ULTRASONIC_PD_COUNT_THRESHOLD:
                self.status += 1
                self.message += f"冷却器侧箱壁超声局部放电次数为{cooler_side_box_wall_ultrasonic_pd_count}，请注意！"
        else:
            self.status = 0
            self.message = "无预警信息。"

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
    model = PdC2h2Model()
    result = model.predict()
    model.generate_alarm_report()
    print(result)
    print("Done")
