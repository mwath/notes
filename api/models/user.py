from __future__ import annotations
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Column, Integer, String, Table, select

from .base import db, metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(320), nullable=False),
    Column("username", String(20), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("totp", String, nullable=True),
    Column("totp_counter", Integer, nullable=True),
)


class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=20)


class UserCreation(UserBase):
    password: constr()

    async def create(user: UserCreation) -> User:
        """
        Create a new user in the database.
        Raise `asyncpg.UniqueViolationError` if the username already exists.
        """
        query = users.insert().values(**user.dict()).returning(users.c.id, users.c.email, users.c.username)
        return User(**await db.fetch_one(query))


class User(UserBase):
    id: int

    async def delete(self) -> Optional[User]:
        if user := await db.fetch_one(users.delete().where(users.c.id == self.id).returning(users)):
            return User(**user)

    async def enable_2fa(self, totp: str):
        await db.execute(users.update().values(totp=totp).where(users.c.id == self.id))

    async def disable_2fa(self):
        await db.execute(users.update().values(totp=None).where(users.c.id == self.id))

    @classmethod
    async def get(cls, username_or_id: Union[int, str]) -> Optional[User]:
        query = select(users.c.id, users.c.email, users.c.username).select_from(users)
        if isinstance(username_or_id, int):
            query = query.where(users.c.id == username_or_id)
        elif isinstance(username_or_id, str):
            query = query.where(users.c.username == username_or_id)
        else:
            raise TypeError(f"must be int or str, not {type(username_or_id)}")

        if user := await db.fetch_one(query):
            return cls(**user)

    @classmethod
    async def get_all(cls) -> list[User]:
        """Return a list of all users"""
        return [cls(**u) for u in await db.fetch_all(users.select())]


class UserPass(User, UserCreation):
    totp: Optional[str]
    totp_counter: Optional[int]

    @classmethod
    async def get(cls, username: str) -> UserPass:
        if user := await db.fetch_one(users.select().where(users.c.username == username)):
            return UserPass(**user)

    async def updateTOTPCounter(self, counter: int | None):
        self.totp_counter = counter
        await db.execute(users.update().values(totp_counter=counter).where(users.c.id == self.id))
