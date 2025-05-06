from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

class MessageCreate(SQLModel):
    name: str = Field(..., min_length=1, max_length=50, description="name, 1-50 characters")
    title: str = Field(..., min_length=1, max_length=100, description="title, 1-100 characters")
    content: str = Field(..., min_length=100, max_length=1000, description="content, 100-1000 characters")
    parent_id: Optional[int] = None

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    parent_id: int | None = Field(default=None, foreign_key="message.id")  
    name: str
    title: str
    content: str
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_approved: bool = Field(default=False)


class PageView(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    count: int = Field(default=0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    # disabled: bool | None = False


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserLogin(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
