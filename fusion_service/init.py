from database import model_info_collection
from utils import upload_file_to_minio
from config import BUCKET_NAME


# 油色谱异常检测模型
def init_oil_chromatography_detection_models():
    models = [
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.XiaoJiang1.HighResistance.A",
            "path": "/潇湘站/油色谱综合异常检测/1000kV潇江Ⅰ线高抗A相",
            "device": "1000kV潇江Ⅰ线高抗A相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV潇江Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.XiaoJiang1.HighResistance.B",
            "path": "/潇湘站/油色谱综合异常检测/1000kV潇江Ⅰ线高抗B相",
            "device": "1000kV潇江Ⅰ线高抗B相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV潇江Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.XiaoJiang1.HighResistance.C",
            "path": "/潇湘站/油色谱综合异常检测/1000kV潇江Ⅰ线高抗C相",
            "device": "1000kV潇江Ⅰ线高抗C相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV潇江Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.XiaoJiang2.HighResistance.A",
            "path": "/潇湘站/油色谱综合异常检测/1000kV潇江Ⅱ线高抗A相",
            "device": "1000kV潇江Ⅱ线高抗A相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV潇江Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.XiaoJiang2.HighResistance.B",
            "path": "/潇湘站/油色谱综合异常检测/1000kV潇江Ⅱ线高抗B相",
            "device": "1000kV潇江Ⅱ线高抗B相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV潇江Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.XiaoJiang2.HighResistance.C",
            "path": "/潇湘站/油色谱综合异常检测/1000kV潇江Ⅱ线高抗C相",
            "device": "1000kV潇江Ⅱ线高抗C相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV潇江Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.JingXiao1.HighResistance.A",
            "path": "/潇湘站/油色谱综合异常检测/1000kV荆潇Ⅰ线高抗A相",
            "device": "1000kV荆潇Ⅰ线高抗A相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV荆潇Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.JingXiao1.HighResistance.B",
            "path": "/潇湘站/油色谱综合异常检测/1000kV荆潇Ⅰ线高抗B相",
            "device": "1000kV荆潇Ⅰ线高抗B相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV荆潇Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.JingXiao1.HighResistance.C",
            "path": "/潇湘站/油色谱综合异常检测/1000kV荆潇Ⅰ线高抗C相",
            "device": "1000kV荆潇Ⅰ线高抗C相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV荆潇Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.JingXiao2.HighResistance.A",
            "path": "/潇湘站/油色谱综合异常检测/1000kV荆潇Ⅱ线高抗A相",
            "device": "1000kV荆潇Ⅱ线高抗A相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV荆潇Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.JingXiao2.HighResistance.B",
            "path": "/潇湘站/油色谱综合异常检测/1000kV荆潇Ⅱ线高抗B相",
            "device": "1000kV荆潇Ⅱ线高抗B相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV荆潇Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.JingXiao2.HighResistance.C",
            "path": "/潇湘站/油色谱综合异常检测/1000kV荆潇Ⅱ线高抗C相",
            "device": "1000kV荆潇Ⅱ线高抗C相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/1000kV荆潇Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.#2MainTransformer.A",
            "path": "/潇湘站/油色谱综合异常检测/#2主变A相",
            "device": "#2主变A相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/#2主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.#2MainTransformer.B",
            "path": "/潇湘站/油色谱综合异常检测/#2主变B相",
            "device": "#2主变B相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/#2主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.#2MainTransformer.C",
            "path": "/潇湘站/油色谱综合异常检测/#2主变C相",
            "device": "#2主变C相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/#2主变C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.#3MainTransformer.A",
            "path": "/潇湘站/油色谱综合异常检测/#3主变A相",
            "device": "#3主变A相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/#3主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.#3MainTransformer.B",
            "path": "/潇湘站/油色谱综合异常检测/#3主变B相",
            "device": "#3主变B相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/#3主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.OilChromatographyDetectionModel.1000kV.#3MainTransformer.C",
            "path": "/潇湘站/油色谱综合异常检测/#3主变C相",
            "device": "#3主变C相",
            "model_name": "油色谱综合异常检测模型",
            "model_type": "oil-chromatography-detection-model",
            "report_path": "report/潇湘站/油色谱/#3主变C相_2021-07-01_2021-07-31.pdf",
        },
    ]

    cron = "2 * * * *"
    for model in models:
        model["schedule"] = cron
    model_info_collection.insert_many(models)
    print("inserted oil chromatography detection models")

    # upload report files to minio
    for model in models:
        upload_file_to_minio(
            bucket_name=BUCKET_NAME,
            object_name=model["report_path"],
            file_path="./assets/特高压换流变油色谱异常处置策略（试行）.pdf",
        )


# 乙炔-氢气含量同步增长模型
def init_c2h2_h2_models():
    models = [
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.XiaoJiang1.HighResistance.A",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅰ线高抗A相",
            "device": "1000kV潇江Ⅰ线高抗A相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.XiaoJiang1.HighResistance.B",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅰ线高抗B相",
            "device": "1000kV潇江Ⅰ线高抗B相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.XiaoJiang1.HighResistance.C",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅰ线高抗C相",
            "device": "1000kV潇江Ⅰ线高抗C相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.XiaoJiang2.HighResistance.A",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅱ线高抗A相",
            "device": "1000kV潇江Ⅱ线高抗A相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.XiaoJiang2.HighResistance.B",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅱ线高抗B相",
            "device": "1000kV潇江Ⅱ线高抗B相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.XiaoJiang2.HighResistance.C",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅱ线高抗C相",
            "device": "1000kV潇江Ⅱ线高抗C相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV潇江Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.JingXiao1.HighResistance.A",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅰ线高抗A相",
            "device": "1000kV荆潇Ⅰ线高抗A相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.JingXiao1.HighResistance.B",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅰ线高抗B相",
            "device": "1000kV荆潇Ⅰ线高抗B相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.JingXiao1.HighResistance.C",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅰ线高抗C相",
            "device": "1000kV荆潇Ⅰ线高抗C相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.JingXiao2.HighResistance.A",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅱ线高抗A相",
            "device": "1000kV荆潇Ⅱ线高抗A相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.JingXiao2.HighResistance.B",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅱ线高抗B相",
            "device": "1000kV荆潇Ⅱ线高抗B相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.JingXiao2.HighResistance.C",
            "path": "/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅱ线高抗C相",
            "device": "1000kV荆潇Ⅱ线高抗C相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/1000kV荆潇Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.#2MainTransformer.A",
            "path": "/潇湘站/乙炔-氢气含量同步增长/#2主变A相",
            "device": "#2主变A相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/#2主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.#2MainTransformer.B",
            "path": "/潇湘站/乙炔-氢气含量同步增长/#2主变B相",
            "device": "#2主变B相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/#2主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.#2MainTransformer.C",
            "path": "/潇湘站/乙炔-氢气含量同步增长/#2主变C相",
            "device": "#2主变C相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/#2主变C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.#3MainTransformer.A",
            "path": "/潇湘站/乙炔-氢气含量同步增长/#3主变A相",
            "device": "#3主变A相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/#3主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.#3MainTransformer.B",
            "path": "/潇湘站/乙炔-氢气含量同步增长/#3主变B相",
            "device": "#3主变B相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/#3主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2H2Model.1000kV.#3MainTransformer.C",
            "path": "/潇湘站/乙炔-氢气含量同步增长/#3主变C相",
            "device": "#3主变C相",
            "model_name": "乙炔-氢气含量同步增长模型",
            "model_type": "c2h2-h2-model",
            "report_path": "report/潇湘站/乙炔-氢气含量同步增长/#3主变C相_2021-07-01_2021-07-31.pdf",
        },
    ]
    cron = "2 * * * *"
    for model in models:
        model["schedule"] = cron

    model_info_collection.insert_many(models)
    print("inserted c2h2 h2 models")

    # upload report files to minio
    for model in models:
        upload_file_to_minio(
            bucket_name=BUCKET_NAME,
            object_name=model["report_path"],
            file_path="./assets/特高压换流变油色谱异常处置策略（试行）.pdf",
        )


# 局放-乙炔同步增长模型
def init_pd_c2h2_models():
    models = [
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.XiaoJiang1.HighResistance.A",
        #     "path": "/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗A相",
        #     "device": "1000kV潇江Ⅰ线高抗A相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        # },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.XiaoJiang1.HighResistance.B",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗B相",
            "device": "1000kV潇江Ⅰ线高抗B相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.XiaoJiang1.HighResistance.C",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗C相",
            "device": "1000kV潇江Ⅰ线高抗C相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.XiaoJiang2.HighResistance.A",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅱ线高抗A相",
            "device": "1000kV潇江Ⅱ线高抗A相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.XiaoJiang2.HighResistance.B",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅱ线高抗B相",
            "device": "1000kV潇江Ⅱ线高抗B相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.XiaoJiang2.HighResistance.C",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅱ线高抗C相",
            "device": "1000kV潇江Ⅱ线高抗C相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV潇江Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.JingXiao1.HighResistance.A",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅰ线高抗A相",
            "device": "1000kV荆潇Ⅰ线高抗A相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.JingXiao1.HighResistance.B",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅰ线高抗B相",
            "device": "1000kV荆潇Ⅰ线高抗B相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.JingXiao1.HighResistance.C",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅰ线高抗C相",
            "device": "1000kV荆潇Ⅰ线高抗C相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.JingXiao2.HighResistance.A",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅱ线高抗A相",
            "device": "1000kV荆潇Ⅱ线高抗A相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.JingXiao2.HighResistance.B",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅱ线高抗B相",
            "device": "1000kV荆潇Ⅱ线高抗B相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.PdC2h2Model.1000kV.JingXiao2.HighResistance.C",
            "path": "/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅱ线高抗C相",
            "device": "1000kV荆潇Ⅱ线高抗C相",
            "model_name": "局放-乙炔同步增长模型",
            "model_type": "pd-c2h2-model",
            "report_path": "report/潇湘站/局放-乙炔同步增长/1000kV荆潇Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.#2MainTransformer.A",
        #     "path": "/潇湘站/局放-乙炔同步增长/#2主变A相",
        #     "device": "#2主变A相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/#2主变A相_2021-07-01_2021-07-31.pdf",
        # },
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.#2MainTransformer.B",
        #     "path": "/潇湘站/局放-乙炔同步增长/#2主变B相",
        #     "device": "#2主变B相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/#2主变B相_2021-07-01_2021-07-31.pdf",
        # },
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.#2MainTransformer.C",
        #     "path": "/潇湘站/局放-乙炔同步增长/#2主变C相",
        #     "device": "#2主变C相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/#2主变C相_2021-07-01_2021-07-31.pdf",
        # },
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.#3MainTransformer.A",
        #     "path": "/潇湘站/局放-乙炔同步增长/#3主变A相",
        #     "device": "#3主变A相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/#3主变A相_2021-07-01_2021-07-31.pdf",
        # },
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.#3MainTransformer.B",
        #     "path": "/潇湘站/局放-乙炔同步增长/#3主变B相",
        #     "device": "#3主变B相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/#3主变B相_2021-07-01_2021-07-31.pdf",
        # },
        # {
        #     "key": "XiaoXiang.PdC2h2Model.1000kV.#3MainTransformer.C",
        #     "path": "/潇湘站/局放-乙炔同步增长/#3主变C相",
        #     "device": "#3主变C相",
        #     "model_name": "局放-乙炔同步增长模型",
        #     "model_type": "pd-c2h2-model",
        #     "report_path": "report/潇湘站/局放-乙炔同步增长/#3主变C相_2021-07-01_2021-07-31.pdf",
        # },
    ]
    cron = "*/5 * * * *"
    for model in models:
        model["schedule"] = cron

    model_info_collection.insert_many(models)
    print("inserted pd c2h2 models")

    # upload report files to minio
    for model in models:
        upload_file_to_minio(
            bucket_name=BUCKET_NAME,
            object_name=model["report_path"],
            file_path="./assets/特高压换流变油色谱异常处置策略（试行）.pdf",
        )


# 油中含气量高且乙炔增长
def init_gas_c2h2_models():
    models = [
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.XiaoJiang1.HighResistance.A",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅰ线高抗A相",
            "device": "1000kV潇江Ⅰ线高抗A相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.XiaoJiang1.HighResistance.B",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅰ线高抗B相",
            "device": "1000kV潇江Ⅰ线高抗B相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.XiaoJiang1.HighResistance.C",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅰ线高抗C相",
            "device": "1000kV潇江Ⅰ线高抗C相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.XiaoJiang2.HighResistance.A",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅱ线高抗A相",
            "device": "1000kV潇江Ⅱ线高抗A相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.XiaoJiang2.HighResistance.B",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅱ线高抗B相",
            "device": "1000kV潇江Ⅱ线高抗B相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.XiaoJiang2.HighResistance.C",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅱ线高抗C相",
            "device": "1000kV潇江Ⅱ线高抗C相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV潇江Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.JingXiao1.HighResistance.A",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅰ线高抗A相",
            "device": "1000kV荆潇Ⅰ线高抗A相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.JingXiao1.HighResistance.B",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅰ线高抗B相",
            "device": "1000kV荆潇Ⅰ线高抗B相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.JingXiao1.HighResistance.C",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅰ线高抗C相",
            "device": "1000kV荆潇Ⅰ线高抗C相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.JingXiao2.HighResistance.A",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅱ线高抗A相",
            "device": "1000kV荆潇Ⅱ线高抗A相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.JingXiao2.HighResistance.B",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅱ线高抗B相",
            "device": "1000kV荆潇Ⅱ线高抗B相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.JingXiao2.HighResistance.C",
            "path": "/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅱ线高抗C相",
            "device": "1000kV荆潇Ⅱ线高抗C相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/1000kV荆潇Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.#2MainTransformer.A",
            "path": "/潇湘站/油中含气量高且乙炔增长/#2主变A相",
            "device": "#2主变A相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/#2主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.#2MainTransformer.B",
            "path": "/潇湘站/油中含气量高且乙炔增长/#2主变B相",
            "device": "#2主变B相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/#2主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.#2MainTransformer.C",
            "path": "/潇湘站/油中含气量高且乙炔增长/#2主变C相",
            "device": "#2主变C相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/#2主变C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.#3MainTransformer.A",
            "path": "/潇湘站/油中含气量高且乙炔增长/#3主变A相",
            "device": "#3主变A相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/#3主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.#3MainTransformer.B",
            "path": "/潇湘站/油中含气量高且乙炔增长/#3主变B相",
            "device": "#3主变B相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/#3主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.GasC2h2Model.1000kV.#3MainTransformer.C",
            "path": "/潇湘站/油中含气量高且乙炔增长/#3主变C相",
            "device": "#3主变C相",
            "model_name": "油中含气量高且乙炔增长模型",
            "model_type": "gas-c2h2-model",
            "report_path": "report/潇湘站/油中含气量高且乙炔增长/#3主变C相_2021-07-01_2021-07-31.pdf",
        },
    ]

    cron = "2 * * * *"
    for model in models:
        model["schedule"] = cron

    model_info_collection.insert_many(models)
    print("inserted gas c2h2 models")

    # upload report files to minio
    for model in models:
        upload_file_to_minio(
            bucket_name=BUCKET_NAME,
            object_name=model["report_path"],
            file_path="./assets/特高压换流变油色谱异常处置策略（试行）.pdf",
        )


# 乙炔呈阶梯型多次增长模型
def init_c2h2_stepwise_increase_models():
    models = [
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.XiaoJiang1.HighResistance.A",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅰ线高抗A相",
            "device": "1000kV潇江Ⅰ线高抗A相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.XiaoJiang1.HighResistance.B",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅰ线高抗B相",
            "device": "1000kV潇江Ⅰ线高抗B相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.XiaoJiang1.HighResistance.C",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅰ线高抗C相",
            "device": "1000kV潇江Ⅰ线高抗C相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.XiaoJiang2.HighResistance.A",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅱ线高抗A相",
            "device": "1000kV潇江Ⅱ线高抗A相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.XiaoJiang2.HighResistance.B",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅱ线高抗B相",
            "device": "1000kV潇江Ⅱ线高抗B相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.XiaoJiang2.HighResistance.C",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅱ线高抗C相",
            "device": "1000kV潇江Ⅱ线高抗C相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV潇江Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.JingXiao1.HighResistance.A",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅰ线高抗A相",
            "device": "1000kV荆潇Ⅰ线高抗A相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.JingXiao1.HighResistance.B",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅰ线高抗B相",
            "device": "1000kV荆潇Ⅰ线高抗B相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅰ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.JingXiao1.HighResistance.C",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅰ线高抗C相",
            "device": "1000kV荆潇Ⅰ线高抗C相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅰ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.JingXiao2.HighResistance.A",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅱ线高抗A相",
            "device": "1000kV荆潇Ⅱ线高抗A相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.JingXiao2.HighResistance.B",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅱ线高抗B相",
            "device": "1000kV荆潇Ⅱ线高抗B相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅱ线高抗B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.JingXiao2.HighResistance.C",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅱ线高抗C相",
            "device": "1000kV荆潇Ⅱ线高抗C相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/1000kV荆潇Ⅱ线高抗C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.#2MainTransformer.A",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/#2主变A相",
            "device": "#2主变A相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/#2主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.#2MainTransformer.B",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/#2主变B相",
            "device": "#2主变B相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/#2主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.#2MainTransformer.C",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/#2主变C相",
            "device": "#2主变C相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/#2主变C相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.#3MainTransformer.A",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/#3主变A相",
            "device": "#3主变A相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/#3主变A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.#3MainTransformer.B",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/#3主变B相",
            "device": "#3主变B相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/#3主变B相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.C2h2StepwiseIncreaseModel.1000kV.#3MainTransformer.C",
            "path": "/潇湘站/乙炔呈阶梯型多次增长/#3主变C相",
            "device": "#3主变C相",
            "model_name": "乙炔呈阶梯型多次增长模型",
            "model_type": "c2h2-stepwise-increase-model",
            "report_path": "report/潇湘站/乙炔呈阶梯型多次增长/#3主变C相_2021-07-01_2021-07-31.pdf",
        },
    ]

    cron = "2 * * * *"
    for model in models:
        model["schedule"] = cron

    model_info_collection.insert_many(models)
    print("inserted c2h2 stepwise increase models")

    # upload report files to minio
    for model in models:
        upload_file_to_minio(
            bucket_name=BUCKET_NAME,
            object_name=model["report_path"],
            file_path="./assets/特高压换流变油色谱异常处置策略（试行）.pdf",
        )


def init_parallel_comparison_models():
    models = [
        {
            "key": "XiaoXiang.ParallelComparisonModel.1000kV.XiaoJiang1.HighResistance",
            "path": "/潇湘站/并行对比/1000kV潇江Ⅰ线高抗",
            "device": "1000kV潇江Ⅰ线高抗",
            "model_name": "横向趋势分析模型",
            "model_type": "parallel-comparison-model",
            "report_path": "report/潇湘站/并行对比/1000kV潇江Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.ParallelComparisonModel.1000kV.XiaoJiang2.HighResistance",
            "path": "/潇湘站/并行对比/1000kV潇江Ⅱ线高抗",
            "device": "1000kV潇江Ⅱ线高抗",
            "model_name": "横向趋势分析模型",
            "model_type": "parallel-comparison-model",
            "report_path": "report/潇湘站/并行对比/1000kV潇江Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.ParallelComparisonModel.1000kV.JingXiao1.HighResistance",
            "path": "/潇湘站/并行对比/1000kV荆潇Ⅰ线高抗",
            "device": "1000kV荆潇Ⅰ线高抗",
            "model_name": "横向趋势分析模型",
            "model_type": "parallel-comparison-model",
            "report_path": "report/潇湘站/并行对比/1000kV荆潇Ⅰ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
        {
            "key": "XiaoXiang.ParallelComparisonModel.1000kV.JingXiao2.HighResistance",
            "path": "/潇湘站/并行对比/1000kV荆潇Ⅱ线高抗",
            "device": "1000kV荆潇Ⅱ线高抗",
            "model_name": "横向趋势分析模型",
            "model_type": "parallel-comparison-model",
            "report_path": "report/潇湘站/并行对比/1000kV荆潇Ⅱ线高抗A相_2021-07-01_2021-07-31.pdf",
        },
    ]

    cron = "2 * * * *"
    for model in models:
        model["schedule"] = cron

    model_info_collection.insert_many(models)
    print("inserted parallel comparison models")

    # upload report files to minio
    for model in models:
        upload_file_to_minio(
            bucket_name=BUCKET_NAME,
            object_name=model["report_path"],
            file_path="./assets/特高压换流变油色谱异常处置策略（试行）.pdf",
        )


def init():
    model_info_collection.drop()
    init_oil_chromatography_detection_models()
    init_c2h2_h2_models()
    init_pd_c2h2_models()
    init_gas_c2h2_models()
    init_c2h2_stepwise_increase_models()
    init_parallel_comparison_models()


if __name__ == "__main__":
    init()
