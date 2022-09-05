from . import models
from .database import engine, get_db

from enum import auto
from pickle import TRUE
from xmlrpc.client import Boolean
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from .routers import posts, user, auth, vote
from .config import settings 

Base = declarative_base()
models.Base.metadata.create_all(bind=engine)


from requests import post

app = FastAPI()


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
{"title": "favorite foods", "content": "pizza", "id": 2}]

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
app.include_router(vote.router)