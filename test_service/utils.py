import requests
from datetime import datetime
import pandas as pd
import asyncio
from pathlib import Path
import os
import aiohttp
from minio import Minio
from pprint import pprint

from database import minio_client

import config


def upload_file_to_minio(bucket_name: str, object_name: str, file_path: str):
    print(
        f"Uploading {file_path} to MinIO bucket {bucket_name} with object name {object_name}"
    )
    # create bucket if not exists
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # check file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    # set content type
    if Path(file_path).suffix == ".pdf":
        content_type = "application/pdf"
    elif Path(file_path).suffix == ".pkl":
        content_type = "application/pickle"
    elif Path(file_path).suffix == ".csv":
        content_type = "text/csv"
    else:
        content_type = "application/octet-stream"

    try:
        minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type,
        )
    except Exception as e:
        print(e)


def fetch_all_expert_model(include="1000kV荆潇Ⅰ线高抗C相", exclude=""):
    url = f"{config.EXPERT_MODEL_URL}/model/info"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"include": include, "exclude": exclude}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(response.text)
    data = response.json()
    if data["code"] != 200:
        raise Exception(data["message"])
    return data["data"]


def predict_model_expert(key):
    url = f"{config.EXPERT_MODEL_URL}/model/predict"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"key": key}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(response.text)
    data = response.json()
    if data["code"] != 200:
        raise Exception(data["message"])
    return data["data"]


def predict_expert(include="1000kV荆潇Ⅰ线高抗C相", exclude=""):
    models = fetch_all_expert_model(include, exclude)
    for model in models:
        key = model["key"]
        print(f"predicting expert model: {key}")
        predict_model_expert(key)
    print("expert model predict success")


def delete_data(start_time, end_time):
    url = f"{config.DATA_SERVICE_URL}/history/delete"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"start_time": start_time, "end_time": end_time}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(response.text)
    data = response.json()
    if data["code"] != 200:
        raise Exception(data["message"])


def fetch_key_by_keyword(include, exclude=""):
    url = f"{config.DATA_SERVICE_URL}/info"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "include": include,
        "exclude": exclude,
        # "exclude_no_unit": False,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(response.text)
    data = response.json()
    if data["code"] != 200:
        raise Exception(data["message"])
    if len(data["data"]) > 1:
        raise Exception("Too many keys found")
    if len(data["data"]) == 0:
        raise Exception(f"No key found for {include}")
    return data["data"][0]


def store_realtime_data(key, value, fresh_time, time):
    if type(fresh_time) is datetime or type(fresh_time) is pd.Timestamp:
        fresh_time = fresh_time.isoformat()
    if type(time) is datetime or type(time) is pd.Timestamp:
        time = time.isoformat()
    url = f"{config.DATA_SERVICE_URL}/realtime/store"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = [{"key": key, "value": value, "fresh_time": fresh_time, "time": time}]
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(response.text)
    data = response.json()
    if data["code"] != 200:
        raise Exception(data["message"])


# rewrite store_realtime_data with async
async def store_realtime_data_async(session, key, value, fresh_time, time):
    if isinstance(fresh_time, (datetime, pd.Timestamp)):
        fresh_time = fresh_time.isoformat()
    if isinstance(time, (datetime, pd.Timestamp)):
        time = time.isoformat()

    url = f"{config.DATA_SERVICE_URL}/realtime/store"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = [{"key": key, "value": value, "fresh_time": fresh_time, "time": time}]

    async with session.post(url, headers=headers, json=data) as response:
        if response.status != 200:
            raise Exception(await response.text())
        data = await response.json()
        if data["code"] != 200:
            raise Exception(data["message"])


# rewrite store_fault_data with async
async def store_fault_data_async(df, device="1000kV潇江Ⅰ线高抗A相"):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            time = row["时间"]
            fresh_time = time

            for colume in df.columns[1:]:
                print(f"store fault data: {device} {colume} {time} {row[colume]}")
                split_colume = colume.split("|")
                include = split_colume[0]
                exclude = ""
                if len(split_colume) > 1:
                    exclude = split_colume[1]
                try:
                    info = fetch_key_by_keyword(
                        include=f"{device}&{include}".replace(" ", ""), exclude=exclude
                    )
                    key = info["key"]
                    value = row[colume]
                    if not pd.isna(value):
                        tasks.append(
                            store_realtime_data_async(
                                session, key, value, fresh_time, time
                            )
                        )
                except Exception as e:
                    print(f"store fault data error: {e}")

        # Run all tasks concurrently
        await asyncio.gather(*tasks)


def store_fault_data(df, device="1000kV潇江Ⅰ线高抗A相", async_mode=True):
    if async_mode:
        asyncio.run(store_fault_data_async(df, device))
    else:
        for index, row in df.iterrows():
            time = row["时间"]
            fresh_time = time

            for colume in df.columns[1:]:
                print(f"store fault data: {device} {colume} {time} {row[colume]}")
                try:
                    info = fetch_key_by_keyword(
                        include=f"{device}&{colume}".replace(" ", ""), exclude=""
                    )
                    key = info["key"]
                    value = row[colume]
                    if not pd.isna(value):
                        store_realtime_data(key, value, fresh_time, time)
                except Exception as e:
                    print(f"store fault data error: {e}")


if __name__ == "__main__":
    df = pd.read_csv("./data/荆潇Ⅰ线高抗C相故障-11:00:00.csv")
    print(df)

    key = fetch_key_by_keyword(include="1000kV潇江Ⅰ线高抗C相&夹件高频局部放电幅值")
    print(key)

    device = "1000kV荆潇Ⅰ线高抗C相"

    import time

    start = time.time()
    store_fault_data(df, device, async_mode=True)
    end = time.time()
    print(f"store_fault_data time: {end-start}")

    # models = fetch_all_expert_model()
    # print(models)
    #
    # key = models[0]["key"]
    # data = predict_model_expert(key)
    # print(data)

    predict_expert()
    delete_data("2099-01-01T00:00:00", "2099-12-30T23:59:59")
