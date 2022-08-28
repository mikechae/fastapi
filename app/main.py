#import sys
#sys.path.insert(0, '/Users/mikechae/Documents/fastapi')
#print(sys.path)

#import os
#print(os.getcwd())

from . import models, utils, schemas, database
import time
from database import engine, get_db
from models import Base

#from "." = current directory
from enum import auto
from pickle import TRUE
from typing import List, Optional
from xmlrpc.client import Boolean

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session





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


@app.get("/")
async def root():
    return{"message": "Sah dude"}

@app.get("/posts", response_model=List[schemas.PostResponse]) 
#"List" allows us to return data in the apprpriate schema

def get_posts(db: Session = Depends(get_db)):
    
    #below is SQL hard code
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    
    #below is ORM query
    posts = db.query(models.Post).all()
    return posts
    
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#include reference to responses in decorator using response_model=nameofmodel

def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES ({post.title},{post.content}, {post.published})""") 
    #above format is not secure, vulernable to SQL injection
    
    #below is SQL hard code
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
#need to commit the changes separately to DB
    #conn.commit()
    
    #below is ORM method
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #db.add(new_post)
    #db.commit()
    #db.refresh(new_post) #this is equivalent to "RETURNING" SQL method

    #more efficient method
    new_post = models.Post(**post.dict()) #unpacking dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #this is equivalent to "RETURNING" SQL method
    return new_post

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post


#get individual object
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): #"int" performs pre-validation via FastAPI
    
    
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) 
    #post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    #instead of using ".all()", this will return first post found matching specified id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found.")
        
        #above option is a cleaner, one-line solution vs the one commented out below
        ## response.status_code = status.HTTP_404_NOT_FOUND
        ## return {'message': f"post with id: {id} was not found."}
    return post

    # deleting post
    # find index in the array that matches the required {id}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    
    post.delete(synchronize_session=False) #default config, read about Session Basics in sqlalchemy doc
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)): 
    #apply "Post" schema outlined before
    #be careful about schema and variable naming conflicts; changed name from "post" to "updated_post"

    
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, 
    #post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() #grab specific post

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist.")

    post_query.update(updated_post.dict(), synchronize_session=False) #need to pas in fields as dictionary

    db.commit()
    return post_query.first()



#create user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
#include reference to responses in decorator using response_model=nameofmodel

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict()) #unpacking dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #this is equivalent to "RETURNING" SQL method
    return new_user


#retrieve user based on id
#many use cases: fetched by front end during authN process

@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)): #"int" performs pre-validation via FastAPI
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"User with id: {id} does not exist.")
    return user
