from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import base64
import json
import os
import requests
import tempfile

from ultralytics import YOLO
#model = YOLO("yolo11n.pt")
model = YOLO("https://hub.ultralytics.com/models/ahJ26xzlb1ncruCZlpTv")
img1_url = "https://ultralytics.com/images/bus.jpg"

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

import psycopg2
connection = psycopg2.connect(database="test", user="postgres", password="postgres", host="pg", port=5432)
cursor = connection.cursor()

@app.get("/")
def root():
    return {"Hello": "World!!!"}

@app.get("/test/")
def test():
    cursor.execute("SELECT * from doc_uri;")
    record = cursor.fetchall()
    return {"data": record}

@app.get("/doc_uri/{item_id}")
def doc_uri(item_id: str, fields: str = "*"):
    cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + item_id + " LIMIT 1;")
    record = cursor.fetchone()
    return { "data": record, "fields": fields, "item_id": item_id }


@app.get("/detect3/{item_id}")
def detect3(item_id: str, fields: str = "uri"):
    url = "https://predict.ultralytics.com"
    headers = {"x-api-key": "222929611344feaab98ebe63d1c232391390749c14"}
    #data0 = {"model": "https://hub.ultralytics.com/models/ahJ26xzlb1ncruCZlpTv", "imgsz": 640, "conf": 0.25, "iou": 0.45}
    data0 = {"model": "https://hub.ultralytics.com/models/ahJ26xzlb1ncruCZlpTv", "imgsz": 640, "conf": 0.25, "iou": 0.45}
    #data = {"jsonData": json.dumps( { "data": data0 } ) }
    data = {"jsonData": json.dumps( data0 ) }
    files = {'file0': ('image.jpg',open('/code/img/image1.jpg', 'rb')),}
    with open("/code/img/image1.jpg") as f:
        response = requests.post(url, headers=headers, data=data, files=files)
    response.raise_for_status()
    # Print inference results
    print(json.dumps(response.json(), indent=2))
    return { "data": response, "item_id": item_id}
    
@app.get("/detect2/{item_id}")
def detect2(item_id: str, fields: str = "uri"):
    #Get the url & prepare for prediction
    cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + item_id + " LIMIT 1;")
    record = cursor.fetchone()
    file_url = record[0]
    file = requests.get(file_url)
    file.raise_for_status()

    #Run prediction
    api_url = "https://predict.ultralytics.com"
    headers = {
        "x-api-key": "222929611344feaab98ebe63d1c232391390749c14",
        "content-type": "application/json"
        }
    #data = {"model": "https://hub.ultralytics.com/models/rEhaHvCC3XPxyaCWAjHj", "imgsz": 640, "conf": 0.25, "iou": 0.45}
    data = {"model": "https://hub.ultralytics.com/models/ahJ26xzlb1ncruCZlpTv", "imgsz": 640, "conf": 0.25, "iou": 0.45}
    #files = [('files',('image.jpg', file.content, 'image/jpeg'))]
    #files = {'file': ('image.jpg', base64.b64encode(file.content))}
    #files = {'file': ('image', file.iter_content(chunk_size=8192), 'image/jpeg')}
    files = {"file": file.content[1:]}
    #data['files'] = file
    #file_data = base64.encode(file)
    response = requests.post(api_url, headers=headers, data=data, files=files)
    #response = requests.post(api_url, headers=headers, data=data, files={("image.jpg",file.content)})
    #response.raise_for_status()

    return { "data": response, "item_id": item_id, "file_url": file_url }

@app.get("/detect/{item_id}")
def detect(item_id: str, fields: str = "uri"):
    results = model(img1_url, save=True, save_txt=True, save_conf=True, verbose=False)
    return { "data": results }
    #Get the uri
    cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + item_id + " LIMIT 1;")
    record = cursor.fetchone()
    file_url = record[0]
    #Download file

    fd, path = tempfile.mkstemp()

    try:
        #Download document as a tmp file
        with os.fdopen(fd, 'wb') as f:
            response = requests.get(record[0], stream=True)
            #response.raise_for_status()
            #for chunk in response.iter_content(chunk_size=8192):
            #    f.write(chunk)
            #Run prediction
            #api_url = "https://predict.ultralytics.com"
            #headers = {"x-api-key": "222929611344feaab98ebe63d1c232391390749c14"}
            #data = {"model": "https://hub.ultralytics.com/models/rEhaHvCC3XPxyaCWAjHj", "imgsz": 640, "conf": 0.25, "iou": 0.45}
            #with open(fd, "rb") as f:
            #    response = requests.post(api_url, headers=headers, data=data, files={"file": f})
            #response.raise_for_status()
    except Exception as e:
        #print(f"Error: {e}")
        # Clean up the temporary file
        os.close(fd)
        os.remove(path)
        # Return an error response
        return {"error": e}
    finally:
        os.close(fd)
        os.remove(path)
        return { "data": "response", "fd": fd, "path": path, "item_id": item_id, "file_url": file_url, "e": e }

    # Check for successful response

    # Print inference results
    #print(json.dumps(response.json(), indent=2))

    if action == "detect":
        url = "https://hub.ultralytics.com/api/v1/models"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    fields = "id, uri"
    cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + item_id + " LIMIT 1;")
    record = cursor.fetchone()
    return { "data": record, "fields": fields, "item_id": item_id }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/detect4/{item_id}")
def detect4(item_id: str, fields: str = "uri"):
    results = model(img1_url, save=True, save_txt=True, save_conf=True, verbose=False)
    return { "data": results.images[0] }
