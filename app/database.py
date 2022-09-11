from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


#SQLALCHEMY_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DB_URL = 'postgres://ccrcrztxpumssc:1f41065ee03eeb15755c942ad38b46d91ad681183eb1b9ac49e816eed9095e77@ec2-3-214-2-141.compute-1.amazonaws.com:5432/dds8lrs6jf0m51'
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
