from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #bcrypt is the algorithm used by passlib

def hash(password: str):
    return pwd_context.hash(password)