from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS
import jwt
import time
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verfiy_password(plain_password,hash_password):
    return pwd_context.verify(plain_password, hash_password)

def create_access_token(data: dict):
    expire = time.time() + 3600
    data.update({"exp": expire})
    print("expire_time: ", expire)
    encoded_jwt = jwt.encode(data, "secret", algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str):
    payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])
    expire_time = payload.get("exp")
    if expire_time <= time.time():
        raise HTTPException(status_code=401, detail= "Token expired. Please Relogin")
    return payload
