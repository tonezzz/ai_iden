from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
def read_root():
    return {"Hello": "World!!!"}

@app.get("/test/")
def test():
    cursor.execute("SELECT * from doc_uri;")
    record = cursor.fetchall()
    return {"data": record}

@app.get("/doc_uri/{item_id}")
def test(item_id: int, fields: str = "*"):
    #cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + item_id + " LIMIT 1;")
    cursor.execute("SELECT %s FROM doc_uri WHERE id=%s LIMIT 1;",(fields,item_id))
    record = cursor.fetchone()
    return { "data": record }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}