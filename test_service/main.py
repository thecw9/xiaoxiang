from fastapi import FastAPI, Body, File, UploadFile
import pandas as pd
from io import BytesIO, StringIO
import traceback
from bson.objectid import ObjectId
import uuid
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from contextlib import asynccontextmanager

from init import init
import config
from database import fault_data_collection
from utils import (
    delete_data,
    minio_client,
    store_fault_data,
    predict_expert,
    delete_data,
    upload_file_to_minio,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init()
    yield
    pass


app = FastAPI(lifespan=lifespan)
app.title = "Model Test API"


class FaultQueryParam(BaseModel):
    include: str = "韶山站&声音&通道1 | 韶山站&声音&通道2"
    exclude: Optional[str] = None


@app.post("/info")
async def get_model_info(params: FaultQueryParam = Body(...)):
    include = params.include
    exclude = params.exclude
    include = params.include.replace(" ", "").replace("AND", "&").replace("OR", "|")
    exclude = params.exclude
    if exclude:
        exclude = exclude.replace(" ", "").replace("AND", "&").replace("OR", "|")

    query = {}
    if include:
        or_items = []
        for item in include.split("|"):
            and_items = []
            for sub_item in item.split("&"):
                and_items.append({"description": {"$regex": sub_item}})
            or_items.append({"$and": and_items})
        query["$or"] = or_items
    if exclude:
        and_items = []
        for item in exclude.split("&"):
            and_items.append({"description": {"$not": {"$regex": item}}})
        query["$and"] = and_items

    model_info = fault_data_collection.find(query)
    model_info = [{**item, "_id": str(item["_id"])} for item in model_info]
    return {
        "code": 200,
        "msg": "success",
        "data": list(model_info),
    }


@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    name: str = Body(...),
    description: str = Body(...),
):
    # upload to minio
    try:
        if file.content_type:
            content_type = file.content_type
        else:
            content_type = "application/octet-stream"
        if file.filename:
            suffix = file.filename.split(".")[-1]
        else:
            suffix = "bin"

        # save to ./fault_data
        tmp_path = f"/tmp/{uuid.uuid4()}.{suffix}"
        with open(tmp_path, "wb") as f:
            f.write(file.file.read())

        object_name = f"fault_data/{name}_{uuid.uuid4()}.{suffix}"
        upload_file_to_minio(config.BUCKET_NAME, object_name, tmp_path)
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    # insert fault_data_collection
    try:
        fault_data_collection.insert_one(
            {
                "name": name,
                "description": description,
                "data_path": object_name,
                "created_at": datetime.now(),
            }
        )
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    return {
        "code": 200,
        "message": "success",
        "data": {"data_path": object_name, "content_type": content_type},
    }


class PredictRequest(BaseModel):
    name: str


@app.post("/predict")
def predict(request: PredictRequest):
    fault_info = fault_data_collection.find_one({"name": request.name})
    if not fault_info:
        return {"status": "error", "message": "data not found"}

    object_name = fault_info["data_path"]

    try:
        response = minio_client.get_object(config.BUCKET_NAME, object_name)
        content = BytesIO(response.read())
        response.close()
        response.release_conn()
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    try:
        df = pd.read_csv(content)
        delete_data("2099-01-01T00:00:00", "2099-12-30T23:59:59")
        store_fault_data(df, device=config.TEST_DEVICE)
        predict_expert(include=config.TEST_DEVICE)
        delete_data("2099-01-01T00:00:00", "2099-12-30T23:59:59")
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    return {"code": 200, "message": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=48021)
