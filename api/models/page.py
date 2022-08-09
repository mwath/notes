from __future__ import annotations
from datetime import datetime

from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, constr
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
    insert,
    update,
    bindparam,
    delete,
    literal_column,
)
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base, db
from .user import User


class DBPage(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(Integer, ForeignKey("users.id"), nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())
    edited = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class DBBlock(Base):
    __tablename__ = "blocks"

    id = Column(String(10), primary_key=True, nullable=False)
    page_id = Column(Integer, ForeignKey("pages.id"), primary_key=True, nullable=False)
    sequence = Column(Integer, unique=True, nullable=False)
    type = Column(String(16), nullable=False)
    data = Column(JSONB, nullable=False)


class PageCreation(BaseModel):
    title: constr(min_length=3, max_length=50, strip_whitespace=True)

    async def create(self, user: User) -> Page:
        query = insert(DBPage).values(title=self.title, author=user.id).returning(DBPage)
        return Page(**await db.fetch_one(query))


class Page(BaseModel):
    id: int
    title: str
    author: int
    created: datetime
    edited: datetime

    @classmethod
    async def get(cls, id: int, user: User) -> Page | None:
        # TODO: Check for permissions
        query = select(DBPage).where(DBPage.id == id)
        return cls(**await db.fetch_one(query))

    @classmethod
    async def get_all(cls, author: User) -> list[Page]:
        """Return a list of all pages created by a user"""
        query = select(DBPage).where(DBPage.author == author.id)
        return [cls(**u) for u in await db.fetch_all(query)]

    async def update(self, **fields) -> Self:
        self.edited = await db.fetch_val(
            update(DBPage).values(**fields).where(DBPage.id == self.id).returning(DBPage.edited)
        )
        return self


