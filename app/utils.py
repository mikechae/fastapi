from pydoc import plain
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #bcrypt is the algorithm used by passlib

def hash(password: str):
    return pwd_context.hash(password)


#function to compare password attempt to hashed password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)