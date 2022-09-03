from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import null
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base): #have to extend "Base" model
    __tablename__ = "posts" #defining tablename

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False) 
    #reference table for FK config
    '''
    #use db migration tool to update table in DB (like alembic)
    #sqlalchemy searches db to find table named posts, if not, it creates it
    #if yes, it leaves it alone
    '''

#class to handle user registration (need to define new postgres table)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True) #unique enables one email per user
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


