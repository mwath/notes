from __future__ import annotations
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Column, Integer, String, insert, select, delete, update

from .base import db, Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String(320), nullable=False)
    username = Column("username", String(20), unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    totp = Column("totp", String, nullable=True)
    totp_counter = Column("totp_counter", Integer, nullable=True)


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
        query = insert(DBUser).values(**user.dict()).returning(DBUser.id, DBUser.email, DBUser.username)
        return User(**await db.fetch_one(query))


class User(UserBase):
    id: int

    async def delete(self) -> Optional[User]:
        if user := await db.fetch_one(delete(DBUser).where(DBUser.id == self.id).returning(DBUser)):
            return User(**user)

    async def enable_2fa(self, totp: str):
        await db.execute(update(DBUser).values(totp=totp).where(DBUser.id == self.id))

    async def disable_2fa(self):
        await db.execute(update(DBUser).values(totp=None).where(DBUser.id == self.id))

    @classmethod
    async def get(cls, username_or_id: Union[int, str]) -> Optional[User]:
        query = select(DBUser.id, DBUser.email, DBUser.username).select_from(DBUser)
        if isinstance(username_or_id, int):
            query = query.where(DBUser.id == username_or_id)
        elif isinstance(username_or_id, str):
            query = query.where(DBUser.username == username_or_id)
        else:
            raise TypeError(f"must be int or str, not {type(username_or_id)}")

        if user := await db.fetch_one(query):
            return cls(**user)

    @classmethod
    async def get_all(cls) -> list[User]:
        """Return a list of all users"""
        return [cls(**u) for u in await db.fetch_all(select(DBUser))]


class UserPass(User, UserCreation):
    totp: Optional[str]
    totp_counter: Optional[int]

    @classmethod
    async def get(cls, username: str) -> UserPass:
        if user := await db.fetch_one(select(DBUser).where(DBUser.username == username)):
            return UserPass(**user)

    async def updateTOTPCounter(self, counter: int | None):
        self.totp_counter = counter
        await db.execute(update(DBUser).values(totp_counter=counter).where(DBUser.id == self.id))
