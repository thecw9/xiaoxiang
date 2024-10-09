import json
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from kafka import KafkaProducer
import config
from utils import get_key_info_by_keywords, fetch_realtime_data, merge_data 

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
)


def ingest_oil_chromatography():
    key_info = get_key_info_by_keywords(["油色谱"])
    keys = [i["key"] for i in key_info]

    data = fetch_realtime_data(keys)

    data = merge_data(key_info, data, key="key")

    # send data to kafka
    for i in data:
        producer.send(config.KAFKA_REALDATA_TOPIC, i)

    producer.flush()
    print("油色谱数据推送成功！")


def ingest_part_discharge():
    key_info_1 = get_key_info_by_keywords(["局部放电"])
    key_info_2 = get_key_info_by_keywords(["局放"])

    key_info = key_info_1 + key_info_2
    # exclude the same key
    key_info = list({i["key"]: i for i in key_info}.values())

    keys = [i["key"] for i in key_info]

    data = fetch_realtime_data(keys)

    data = merge_data(key_info, data, key="key")

    # send data to kafka
    for i in data:
        producer.send(config.KAFKA_REALDATA_TOPIC, i)

    producer.flush()
    print("局部放电数据推送成功！")


def ingest_iron_core():
    key_info = get_key_info_by_keywords(["接地", "电流"])
    keys = [i["key"] for i in key_info]

    data = fetch_realtime_data(keys)

    data = merge_data(key_info, data, key="key")

    # send data to kafka
    for i in data:
        producer.send(config.KAFKA_REALDATA_TOPIC, i)

    producer.flush()
    print("铁芯夹件数据推送成功！")


ingest_oil_chromatography()
ingest_part_discharge()
ingest_iron_core()

scheduler = BlockingScheduler()
trigger = CronTrigger(minute=0)

scheduler.add_job(ingest_oil_chromatography, trigger)
scheduler.add_job(ingest_part_discharge, IntervalTrigger(minutes=5))
scheduler.add_job(ingest_iron_core, trigger)

scheduler.start()
