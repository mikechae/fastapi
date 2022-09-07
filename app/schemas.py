from typing import Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

from .database import Base


# request "Get" method url: "/"
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
        orm_mode=True


class PostCreate(PostBase): #inherits all fields of the model it extends via "PostBase" in this example
    pass

#when updating, we want user to specify all changes, don't set default value in these situations

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

    #we left out password as the user has no need to see their password


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut  #can return pydantic model
    
    class Config:
        orm_mode = True


#below models are for responses back to user
class PostResponse(PostBase): 
    #can eliminate duplicate values, extend other model with same fields (i.e. id, title, and content)
    #if not extending other model to prevent duplication, needs to extend the BaseModel
    
    id: int
    created_at: datetime
    user_id: int  #automatically grabs field from db
    class Config:
        orm_mode=True

    #need to include above two lines when output is a pydantic model as the
    #model by default is not a dictionary
    
class PostOut(BaseModel):
    Post: Post #references schema for returning post data
    votes: int       
    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)