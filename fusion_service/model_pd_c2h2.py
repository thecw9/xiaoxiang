import uuid
from config import BUCKET_NAME
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import math
import redis

from database import redis_pool
from utils import (
    fetch_measure_detail,
    fetch_measure_info_by_keyword,
    fetch_realtime_data,
    save_markdown_to_pdf,
    upload_file_to_minio,
    fetch_history_data,
    fetch_latest_history_data,
    is_over_single_model_threshold,
)


class PdC2h2Model:
    def __init__(
        self,
        path="/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗A相",
        device="1000kV荆潇Ⅰ线高抗C相",
        alarm_report_path="alarm_report.pdf",
    ):
        self.path = path
        self.device = device
        self.alarm_report_path = alarm_report_path

        self.data_limit = 30
        self.C2H2_THRESHOLD = 0.05

        self.HIGHFREQPD_AMPLITUDE_ABSOLUTE_THRESHOLD = 0.1  # 100mV = 0.1V
        self.HIGHFREQPD_AMPLITUDE_TRIGGER_THRESHOLD = 0.05  # 50mV = 0.05V
        self.HIGHFREQPD_AMPLITUDE_RELATED_THRESHOLD = 5  # 5倍
        self.HIGHFREQPD_COUNT_TRIGGER_THRESHOLD = 2000 * 5  # 2000次/min * 5min
        self.HIGHFREQPD_COUNT_RELATED_THRESHOLD = 10  # 10倍

        self.ULTRASONICPD_AMPLITUDE_TRIGGER_THRESHOLD = 500  # 500mV
        self.ULTRASONICPD_AMPLITUDE_ABSOLUTE_THRESHOLD = 1000  # 1000mV
        self.ULTRASONICPD_AMPLITUDE_RELATED_THRESHOLD = 5  # 5倍
        self.ULTRASONICPD_COUNT_RELATED_THRESHOLD = 50  # 50次/5min

        self.r = redis.Redis(connection_pool=redis_pool)

        self.highfreq_data = {}
        self.ultrasonic_data = {}
        self.oil_chromatography_data = {}

        self.message = ""
        self.status = 0

    def is_highfreq_trigger(self, position: str = "夹件"):
        pd_amp_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}高频局部放电幅值"
        )
        pd_amp_key = pd_amp_info["key"]
        pd_amplitude_json = fetch_realtime_data(pd_amp_key)
        print(position)
        print(pd_amplitude_json)
        pd_amplitude = pd_amplitude_json["value"]

        pd_count_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}高频局部放电次数"
        )
        pd_count_key = pd_count_info["key"]
        pd_count_json = fetch_realtime_data(pd_count_key)
        pd_count = pd_count_json["value"]

        if pd_amplitude > self.HIGHFREQPD_AMPLITUDE_TRIGGER_THRESHOLD:
            return True

    def is_ultrasonic_trigger(self, position: str = "夹件"):
        pd_amp_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}超声局部放电幅值"
        )
        pd_amp_key = pd_amp_info["key"]
        pd_amplitude_json = fetch_realtime_data(pd_amp_key)
        pd_amplitude = pd_amplitude_json["value"]

        pd_count_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}超声局部放电次数"
        )
        pd_count_key = pd_count_info["key"]
        pd_count_json = fetch_realtime_data(pd_count_key)
        pd_count = pd_count_json["value"]

        if pd_amplitude > self.ULTRASONICPD_AMPLITUDE_TRIGGER_THRESHOLD:
            return True

    def diagnose_highfreq_pd(self, position: str = "夹件"):
        data_limit = 6
        PD_AMP_THRESHOLD = self.HIGHFREQPD_AMPLITUDE_ABSOLUTE_THRESHOLD
        PD_AMP_RELATED_THRESHOLD = self.HIGHFREQPD_AMPLITUDE_RELATED_THRESHOLD
        PD_COUNT_RELATED_THRESHOLD = self.HIGHFREQPD_COUNT_RELATED_THRESHOLD

        init_status = self.status

        pd_amp_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}高频局部放电幅值"
        )
        pd_amp_key = pd_amp_info["key"]
        pd_amplitude_json = fetch_latest_history_data(pd_amp_key, limit=data_limit)
        self.highfreq_data[f"{pd_amp_key}"] = pd_amplitude_json
        pd_amplitude = pd_amplitude_json[0]["value"]
        if (
            pd_amplitude > PD_AMP_THRESHOLD
            and is_over_single_model_threshold(pd_amp_key) >= 0
        ):
            self.status += 1
            pd_amplitude = round(pd_amplitude, 4)
            self.message += f"<b>{position}高频局部放电幅值</b>(编号：{pd_amp_key}，实时值：{pd_amplitude,4})超过阈值{PD_AMP_THRESHOLD}。\n"

        # 如果绝对值判断已经报警，则不再进行相对值判断
        if self.status > init_status:
            return

        # 相对值判断
        # 获取7天前一天的数据
        start_time_7_days_ago = datetime.now() - timedelta(days=7)
        end_time_7_days_ago = start_time_7_days_ago + timedelta(days=1)

        pd_amplitude_7_days_ago_json = fetch_history_data(
            pd_amp_info["key"],
            start_time=start_time_7_days_ago,
            end_time=end_time_7_days_ago,
        )
        mean_pd_amplitude_7_days_ago = np.mean(
            [x["value"] for x in pd_amplitude_7_days_ago_json]
        )

        pd_count_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}高频局部放电次数"
        )
        pd_count_key = pd_count_info["key"]
        pd_count_json = fetch_latest_history_data(pd_count_key, limit=data_limit)
        self.highfreq_data[f"{pd_count_key}"] = pd_count_json
        pd_count = pd_count_json[0]["value"]

        pd_count_7_days_ago_json = fetch_history_data(
            pd_count_info["key"],
            start_time=start_time_7_days_ago,
            end_time=end_time_7_days_ago,
        )
        mean_pd_count_7_days_ago = np.mean(
            [x["value"] for x in pd_count_7_days_ago_json]
        )

        if (
            pd_amplitude > mean_pd_amplitude_7_days_ago * PD_AMP_RELATED_THRESHOLD
            and pd_count > mean_pd_count_7_days_ago * PD_COUNT_RELATED_THRESHOLD
        ):
            self.status += 1
            pd_amplitude = round(pd_amplitude, 4)
            mean_pd_amplitude_7_days_ago = round(mean_pd_amplitude_7_days_ago, 4)
            self.message += (
                f"<b>{position}高频局部放电幅值</b>(编号：{pd_amp_info['key']}，实时值：{pd_amplitude})超过7天前的均值{mean_pd_amplitude_7_days_ago}的{PD_AMP_RELATED_THRESHOLD}倍；"
                + f"<b>{position}高频局部放电次数</b>(编号：{pd_count_info['key']}，实时值：{pd_count})超过7天前的均值{mean_pd_count_7_days_ago}的{PD_COUNT_RELATED_THRESHOLD}倍。\n"
            )

    def diagnose_ultrasonic_pd(self, position: str = "夹件"):
        data_limit = 6
        PD_AMP_THRESHOLD = self.ULTRASONICPD_AMPLITUDE_ABSOLUTE_THRESHOLD
        PD_AMP_RELATED_THRESHOLD = self.ULTRASONICPD_AMPLITUDE_RELATED_THRESHOLD

        init_status = self.status

        pd_amp_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}超声局部放电幅值"
        )
        pd_amp_key = pd_amp_info["key"]
        pd_amplitude_json = fetch_latest_history_data(pd_amp_key, limit=data_limit)
        self.ultrasonic_data[f"{pd_amp_key}"] = pd_amplitude_json
        pd_amplitude = pd_amplitude_json[0]["value"]
        if (
            abs(pd_amplitude) > PD_AMP_THRESHOLD
            and is_over_single_model_threshold(key=pd_amp_key) >= 0
        ):
            self.status += 1
            self.message += f"<b>{position}超声局部放电幅值</b>(编号：{pd_amp_key}，实时值：{pd_amplitude})超过阈值{PD_AMP_THRESHOLD}。\n"

        # 如果绝对值判断已经报警，则不再进行相对值判断
        if self.status > init_status:
            return

        # 相对值判断
        # 获取7天前一天的超声局部放电幅值数据
        start_time_7_days_ago = datetime.now() - timedelta(days=7)
        end_time_7_days_ago = start_time_7_days_ago + timedelta(days=1)
        pd_amplitude_7_days_ago_json = fetch_history_data(
            pd_amp_info["key"], start_time_7_days_ago, end_time_7_days_ago
        )
        mean_pd_amplitude_7_days_ago = np.mean(
            np.abs([x["value"] for x in pd_amplitude_7_days_ago_json])
        )

        # 获取超声局部放电次数
        pd_count_info = fetch_measure_info_by_keyword(
            include=f"{self.device}&{position}超声局部放电次数"
        )
        pd_count_key = pd_count_info["key"]
        high_frequency_pd_count_json = fetch_latest_history_data(
            pd_count_key, limit=self.data_limit
        )
        self.ultrasonic_data[f"{pd_count_key}"] = high_frequency_pd_count_json
        pd_count = high_frequency_pd_count_json[0]["value"]

        if (
            abs(pd_amplitude) > mean_pd_amplitude_7_days_ago * PD_AMP_RELATED_THRESHOLD
            and pd_count > self.ULTRASONICPD_COUNT_RELATED_THRESHOLD
        ):
            self.status += 1
            self.message += (
                f"<b>{position}超声局部放电幅值</b>(编号：{pd_amp_info['key']}，实时值：{pd_amplitude})超过7天前的均值{mean_pd_amplitude_7_days_ago}的{PD_AMP_RELATED_THRESHOLD}倍；"
                + f"<b>{position}超声局部放电次数</b>(编号：{pd_count_info['key']}，实时值：{pd_count})超过阈值{self.ULTRASONICPD_COUNT_RELATED_THRESHOLD}。\n"
            )

    def predict(self) -> dict:
        # 1. 获取最新的历史数据

        # 高频局部放电触发
        if (
            self.is_highfreq_trigger("高压套管升高座")
            or self.is_highfreq_trigger("夹件")
            or self.is_highfreq_trigger("铁芯")
        ):
            self.r.set(f"{self.device}_highfreq_trigger", 1)  # 存储触发标志
            self.r.expire(f"{self.device}_highfreq_trigger", 60 * 35)  # 35分钟过期

        # 判断是否触发，如果触发则进行诊断
        if self.r.exists(f"{self.device}_highfreq_trigger"):
            self.diagnose_highfreq_pd("高压套管升高座")
            self.diagnose_highfreq_pd("夹件")
            self.diagnose_highfreq_pd("铁芯")

        # 超声局部放电触发
        if (
            self.is_ultrasonic_trigger("高压侧出线装置幅向")
            or self.is_ultrasonic_trigger("高压侧出线装置L弯")
            or self.is_ultrasonic_trigger("高压侧出线装置轴向")
            or self.is_ultrasonic_trigger("高压侧出线装置&箱壁")
            or self.is_ultrasonic_trigger("高压套管末屏")
            or self.is_ultrasonic_trigger("冷却器对侧箱壁")
            or self.is_ultrasonic_trigger("铁芯夹件侧箱壁")
            or self.is_ultrasonic_trigger("冷却器侧箱壁")
        ):
            self.r.set(f"{self.device}_ultrasonic_trigger", 1)  # 存储触发标志
            self.r.expire(f"{self.device}_ultrasonic_trigger", 60 * 35)  # 35分钟过期

        # 判断是否触发, 如果触发则进行诊断
        if self.r.exists(f"{self.device}_ultrasonic_trigger"):
            self.diagnose_ultrasonic_pd("高压侧出线装置幅向")
            self.diagnose_ultrasonic_pd("高压侧出线装置L弯")
            self.diagnose_ultrasonic_pd("高压侧出线装置轴向")
            self.diagnose_ultrasonic_pd("高压侧出线装置&箱壁")
            self.diagnose_ultrasonic_pd("高压套管末屏")
            self.diagnose_ultrasonic_pd("冷却器对侧箱壁")
            self.diagnose_ultrasonic_pd("铁芯夹件侧箱壁")
            self.diagnose_ultrasonic_pd("冷却器侧箱壁")

        # 如果有局部放电报警，则存储到redis，用于后续判断乙炔和局部放电是否同步增长
        if self.status > 0:
            self.status = 1
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.message = f"<b>{now}</b>\n {self.message}"
            # add to redis alarm list
            self.r.rpush(f"{self.device}_pd_alarm_list", self.message)
            self.r.expire(f"{self.device}_pd_alarm_list", 60 * 60 * 24)  # 24小时过期

        # 乙炔数据
        info = fetch_measure_info_by_keyword(
            include=f"{self.device}&第二套油色谱在线监测_C2H2"
        )
        c2h2_measurement_json = fetch_latest_history_data(info["key"], limit=10)
        self.oil_chromatography_data[f"{info['key']}"] = c2h2_measurement_json
        # check if c2h2 increase
        c2h2_increments_2h = (
            c2h2_measurement_json[0]["value"] - c2h2_measurement_json[2]["value"]
        )
        # check pd_alarm_list exist
        pd_alarm_list = self.r.lrange(f"{self.device}_pd_alarm_list", 0, -1)
        pd_alarm_list = [x.decode("utf-8") for x in pd_alarm_list]
        if c2h2_increments_2h >= self.C2H2_THRESHOLD and len(pd_alarm_list) > 0:
            self.status = 3
            pd_alarm_info = "\n".join(pd_alarm_list[::-1])
            self.message = f"<b>乙炔和局部放电出现同步增长。</b> \n乙炔2小时增长量超过阈值{self.C2H2_THRESHOLD}，\n局部放电报警信息：\n{pd_alarm_info}"

        # 3. 生成报告
        if self.status > 0:
            self.generate_alarm_report()

        if self.status == 0:
            self.message = "未发现异常"

        # 4. 返回结果
        return {
            "status": self.status,
            "message": self.message,
        }

    def convert_data_to_markdown(self, data: dict):
        if len(data) == 0:
            return ""
        # convert to DataFrame
        df_list = []
        for key, value in data.items():
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

        return data_markdown

    def generate_alarm_report(self):
        # tmp_file_dir = "/tmp/test"
        print("generate report")
        tmp_file_dir = f"/tmp/{uuid.uuid4()}"
        os.makedirs(tmp_file_dir, exist_ok=True)

        highfreq_data_markdown = self.convert_data_to_markdown(self.highfreq_data)
        ultrasonic_data_markdown = self.convert_data_to_markdown(self.ultrasonic_data)
        oil_chromatography_data_markdown = self.convert_data_to_markdown(
            self.oil_chromatography_data
        )

        text = f"""
# {self.path}诊断报告

## 监测数据

### 高频局部放电数据
{highfreq_data_markdown}

### 超声局部放电数据
{ultrasonic_data_markdown}

### 油色谱数据
{oil_chromatography_data_markdown}

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
    print(result)
    print("Done")
