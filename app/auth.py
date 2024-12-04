from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

# 定义 secret key 和加密算法
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# 密码加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 路由器
router = APIRouter()


class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# 存储用户信息
fake_users_db = {}


# 生成 JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 用户验证
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# 用户注册
@router.post("/register")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    fake_users_db[user.username] = get_password_hash(user.password)
    return {"msg": "User registered successfully"}


# 用户登录并生成 JWT
@router.post("/login", response_model=Token)
def login_for_access_token(user: User):
    if user.username not in fake_users_db or not verify_password(user.password, fake_users_db[user.username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
