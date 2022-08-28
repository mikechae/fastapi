from typing import Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from .database import Base


# request "Get" method url: "/"
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
        orm_mode=True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase): #inherits all fields of the model it extends via "PostBase" in this example
    pass

#when updating, we want user to specify all changes, don't set default value in these situations


#below models are for responses back to user
class PostResponse(PostBase): 
    #can eliminate duplicate values, extend other model with same fields (i.e. id, title, and content)
    #if not extending other model to prevent duplication, needs to extend the BaseModel
    
    id: int
    created_at: datetime
    class Config:
        orm_mode=True

    #need to include above two lines when output is a pydantic model as the
    #model by default is not a dictionary
    
     
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode=True
    #we left out password as the user has no need to see their password

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None