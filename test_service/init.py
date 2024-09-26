from database import fault_data_collection
import uuid
from utils import upload_file_to_minio

from config import BUCKET_NAME


def init():
    fault_data_collection.drop()

    fault = {
        "name": "500 千伏常岗线高抗C 相故障-04:00:00",
        "description": """2024 年7 月12 日，国网湖南超高压变电公司在500 千伏岗市站常岗线C 相高抗检出油中乙炔0.1μL/L、总烃25.5μL/L，复测数据一致。与上次（5 月24 日）相比，新增乙炔，且氢气、甲烷、一氧化碳、二氧化碳均有增长。根据特征气体法，判断高抗内部存在局部放电缺陷，故障可能涉及固体绝缘材料。
常岗线高抗为陕西省西安变压器厂生产，型号BKD-50000/500，2001 年8 月出厂，同年10 月30 日投入运行，运行已超22 年。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME,
        fault["data_path"],
        "./data/500 千伏常岗线高抗C 相故障-04:00:00.csv",
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-01:00:00",
        "description": """超声波法监测结果显示，从10月26日00:55时起，超声波法开始监测到异常信号。通道0（L型高压套管升高座幅向）、通道1（L型高压套管升高座L型折弯处）、通道2（L型高压套管升高座轴向）、通道4（套管末屏）监测到的超声波信号较强烈，通道1和通道2的信号幅值较大。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-01:00:00.csv"
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-01:45:00",
        "description": """超声波法监测结果显示，从10月26日00:55时起，超声波法开始监测到异常信号。通道0（L型高压套管升高座幅向）、通道1（L型高压套管升高座L型折弯处）、通道2（L型高压套管升高座轴向）、通道4（套管末屏）监测到的超声波信号较强烈，通道1和通道2的信号幅值较大。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-01:45:00.csv"
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-03:15:00",
        "description": """高频法监测结果显示，2022年10月25有监视到疑似放电信号，但是信号幅值很小，图谱特征与干扰近似。因此排除。从2022年10月26日1：20起，高频法开始监测到异常信号，通道1（夹件接地）和通道2（铁芯接地）监测到的高频信号较强烈，通道2的信号幅值较大，说明该高抗本体内存在局部放电，且放电源位置靠近铁芯。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-03:15:00.csv"
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-03:30:00",
        "description": """高频法监测结果显示，2022年10月25有监视到疑似放电信号，但是信号幅值很小，图谱特征与干扰近似。因此排除。从2022年10月26日1：20起，高频法开始监测到异常信号，通道1（夹件接地）和通道2（铁芯接地）监测到的高频信号较强烈，通道2的信号幅值较大，说明该高抗本体内存在局部放电，且放电源位置靠近铁芯。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-03:30:00.csv"
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-03:35:00",
        "description": """高频法监测结果显示，2022年10月25有监视到疑似放电信号，但是信号幅值很小，图谱特征与干扰近似。因此排除。从2022年10月26日1：20起，高频法开始监测到异常信号，通道1（夹件接地）和通道2（铁芯接地）监测到的高频信号较强烈，通道2的信号幅值较大，说明该高抗本体内存在局部放电，且放电源位置靠近铁芯。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-03:35:00.csv"
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-07:05:00",
        "description": """高频法监测结果显示，2022年10月25有监视到疑似放电信号，但是信号幅值很小，图谱特征与干扰近似。因此排除。从2022年10月26日1：20起，高频法开始监测到异常信号，通道1（夹件接地）和通道2（铁芯接地）监测到的高频信号较强烈，通道2的信号幅值较大，说明该高抗本体内存在局部放电，且放电源位置靠近铁芯。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-07:05:00.csv"
    )

    fault = {
        "name": "1000 千伏潇湘站荆潇Ⅰ线高抗C相故障-11:00:00",
        "description": """潇湘站2022年10月26日上午，荆潇Ⅰ线高抗C相综合监测装置显示，超声波法、高频法和油色谱法均监测到了异常情况，设备于下午6点停电。异常数据分析梳理如下。
超声波法监测结果显示，从10月26日00:55时起，超声波法开始监测到异常信号。通道0（L型高压套管升高座幅向）、通道1（L型高压套管升高座L型折弯处）、通道2（L型高压套管升高座轴向）、通道4（套管末屏）监测到的超声波信号较强烈，通道1和通道2的信号幅值较大。
高频法监测结果显示，2022年10月25有监视到疑似放电信号，但是信号幅值很小，图谱特征与干扰近似。因此排除。从2022年10月26日1：20起，高频法开始监测到异常信号，通道1（夹件接地）和通道2（铁芯接地）监测到的高频信号较强烈，通道2的信号幅值较大，说明该高抗本体内存在局部放电，且放电源位置靠近铁芯。
综合监测装置显示，2022年10月26日6时起，荆潇Ⅰ线高抗C相开始产生特征气体H2和C2H2，并持续增长，在11时达到0.5的告警值，综合监测油色谱超阈值告警。
""",
        "data_path": f"fault_data/{uuid.uuid4()}.csv",
    }
    fault_data_collection.insert_one(fault)
    upload_file_to_minio(
        BUCKET_NAME, fault["data_path"], "./data/荆潇Ⅰ线高抗C相故障-11:00:00.csv"
    )
