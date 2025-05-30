from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import base64
import io
import json
import os
import requests
import tempfile

from ultralytics import YOLO
#model = YOLO("yolo11n.pt")
model = YOLO("https://hub.ultralytics.com/models/ahJ26xzlb1ncruCZlpTv")
img1_url = "https://ultralytics.com/images/bus.jpg"

import db
cursor = db.open()

# FastAPI application with CORS and PostgreSQL connection

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Hello": "World!!!"}

@app.get("/image/{id}")
def img(id: str, fields: str = "*"):
    #cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + id + " LIMIT 1;")
    #record = cursor.fetchone()
    return { "data": get_img(id,fields) }

###########
@app.get("/detect/{id}")
async def detect(id: str, fields: str = "uri"):
    img_url = get_img_url(id)
    results = model(img_url)
    result = results[0]
    return results[0][0].to_json(normalize=True)

###########
@app.get("/detect2/{id}")
async def detect2(id: str, fields: str = "uri"):
    img_url = get_img_url(id)
    results = model(img_url)
    result = results[0][0].to_json(normalize=True)

    for result in results[0]:
        output = dict()
        output['class'] = result.cls
        result.ap
    return output
    #return { results[0][0].to_json(normalize=True) {}


@app.get("/test/")
def test():
    cursor.execute("SELECT * from doc_uri;")
    record = cursor.fetchall()
    return {"data": record}

def get_img(id,fields="*"):
    cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + id + " LIMIT 1;")
    record = cursor.fetchone()
    if record:
        return record
    else:
        return None 

def get_img_url(id):
    return get_img(id, "uri")

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
import io

def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

def init_db(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doc_uri (
            id SERIAL PRIMARY KEY,
            uri TEXT NOT NULL
        );
    """)
    connection.commit()
    # Insert a sample image URI if the table is empty
    cursor.execute("SELECT COUNT(*) FROM doc_uri;")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO doc_uri (uri) VALUES ('https://ultralytics.com/images/bus.jpg');")
        connection.commit()
