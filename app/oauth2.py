from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET_KEY
#Algorithm
#Token Expiration time
# 

SECRET_KEY = "as2kjhw495j351l1kjlfadf024359384694857234345dasdfkaj2l"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy() #want to make copy of data to prevent changing original

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #insert expiration time into token

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #can pass jwt token into https://jwt.io/ to decode token
    return encoded_jwt