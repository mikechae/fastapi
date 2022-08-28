from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer #for oauth2scheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #from path op decorator

#SECRET_KEY
#Algorithm
#Token Expiration time
# 

#store as env variables, not hard coded
SECRET_KEY = "as2kjhw495j351l1kjlfadf024359384694857234345dasdfkaj2l"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy() #want to make copy of data to prevent changing original

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #insert expiration time into token

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #can pass jwt token into https://jwt.io/ to decode token
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    return token_data


#validate token, extract user id, 
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)