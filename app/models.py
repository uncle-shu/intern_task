import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: uuid.UUID


class Task(SQLModel):
    id: int = Field(primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    status: str
    source_language: str
    target_language: str
    original_content: str
    translated_content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class TaskCreate(SQLModel):
    source_language: str
    target_language: str
    original_content: str


class TaskStatus(SQLModel):
    status: str
    translated_content: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
