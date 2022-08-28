from .. import models, schemas, utils
from fastapi import status
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)): #"int" performs pre-validation via FastAPI
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"User with id: {id} does not exist.")
    return user
