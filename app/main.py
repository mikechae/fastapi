from . import schemas, utils, database, models
import time
from .database import engine, get_db

#from "." = current directory
from enum import auto
from pickle import TRUE
from typing import List, Optional
from xmlrpc.client import Boolean

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from .routers import posts, user, auth

Base = declarative_base()
models.Base.metadata.create_all(bind=engine)


from requests import post

app = FastAPI()



#connecting to DB
while True:

    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='se7olutioN',
        cursor_factory=RealDictCursor) # "cursor_factory" returns column names, which is not shows by default
        cursor = conn.cursor()
        print("Database Connection Successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
{"title": "favorite foods", "content": "pizza", "id": 2}]


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # making a query using ORM
    post = db.query(models.Post).all()
    return {"data": post}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p    

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(posts.router) #when get HTTP request, include posts.router when going down list
app.include_router(user.router)
app.include_router(auth.router)
