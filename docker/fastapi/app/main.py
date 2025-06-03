from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import base64
import io
import json
import os
import requests
import tempfile


app = FastAPI()

from .http import *
http_init(app)
from .model import *
model = model_init()
from .db import *
cursor = db_init()

@app.get("/")
def root():
    return {"Hello": "World!!!"}

@app.get("/image/{id}")
def img(id: str, fields: str = "*"):
    return db_get_img(cursor,id,fields)

###########
@app.get("/detect/{id}")
async def detect(id: str, fields: str = "uri"):
    img_url = db_get_img_url(cursor,id)
    results = model(img_url)
    return results[0][0].to_json(normalize=True)

###########
@app.get("/detect2/{id}")
async def detect2(id: str, fields: str = "uri"):
    img_url = db_get_img_url(cursor,id)
    results = model_detect(model,img_url)
    if(results.boxes):
        return JSONResponse(content=jsonable_encoder(results))
    #return json.dumps(results)
    #rs = json.loads(results[0].to_json() )
    #ret = []
    #for result in rs:
    #    item = list(result)
    #    ret.append(item)
    #return ret
    #return { results[0][0].to_json(normalize=True) {}

###########
@app.get("/yolo/detect/{id}")
async def yolo_detect(id: str, fields: str = "uri"):
    img_url = db_get_img_url(cursor,id)
    api_url = "http://yolo:8103/detect"
    response = requests.get(api_url, params={"id": id, "fields": fields})
    return response
    #results = model_detect(model,img_url)
    #if(results.boxes):
    #    return JSONResponse(content=jsonable_encoder(results))
