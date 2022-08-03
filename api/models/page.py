from __future__ import annotations
from datetime import datetime

from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, constr
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, select, insert, update
from sqlalchemy.sql import func

from .base import Base, db
from .user import User


class DBPage(Base):
    __tablename__ = "pages"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(50), nullable=False)
    author = Column("author", Integer, ForeignKey("users.id"), nullable=False)
    content = Column("content", String(20000), nullable=False, server_default="")
    created = Column("created", DateTime, nullable=False, server_default=func.now())
    edited = Column("edited", DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class PageCreation(BaseModel):
    title: constr(min_length=3, max_length=50, strip_whitespace=True)

    async def create(self, user: User) -> Page:
        query = insert(DBPage).values(title=self.title, author=user.id).returning(DBPage)
        return Page(**await db.fetch_one(query))


class Page(BaseModel):
    id: int
    title: str
    author: int
    content: str
    created: datetime
    edited: datetime

    @classmethod
    async def get(cls, id: int, user: User) -> Optional[Page]:
        # TODO: Check for permissions
        query = select(DBPage).where(DBPage.id == id)
        return await db.fetch_one(query)

    @classmethod
    async def get_all(cls, author: User) -> list[Page]:
        """Return a list of all pages created by a user"""
        query = select(DBPage).where(DBPage.author == author.id)
        return [cls(**u) for u in await db.fetch_all(query)]

    async def updateTitle(self, title: str) -> Self:
        query = update(DBPage).values(title=title).where(DBPage.id == self.id).returning(DBPage.edited)
        self.edited = await db.fetch_val(query)
        return self

    async def updateContent(self, content: str) -> Self:
        query = update(DBPage).values(content=content).where(DBPage.id == self.id).returning(DBPage.edited)
        self.edited = await db.fetch_val(query)
        return self

