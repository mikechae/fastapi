from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


SQLALCHEMY_DB_URL = 'postgresql://postgres:se7olutioN@localhost/fastapi'
#not good to harcode these values in the code

engine = create_engine(SQLALCHEMY_DB_URL)


#connecting to DB
''' 
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

'''
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#above values are default values

Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
