from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, constr
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    bindparam,
    delete,
    insert,
    literal_column,
    select,
    true,
    update,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from .base import Base, db
from .user import User


class DBPage(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(Integer, ForeignKey("users.id"), nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())
    edited = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    active = Column(Boolean, nullable=False, server_default=true())


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
    active: bool

    @classmethod
    async def get(cls, id: int, user: User) -> Page | None:
        # TODO: Check for permissions
        query = select(DBPage).where(DBPage.id == id)
        return cls(**await db.fetch_one(query))

    @classmethod
    async def update(cls, page_id: int, page: PageCreation, user: User) -> Page | None:
        if page := await db.fetch_one(
            update(DBPage).values(title=page.title).where(DBPage.id == page_id).returning(DBPage)
        ):
            return cls(**page)

    @classmethod
    async def delete(cls, id: int, user: User) -> Page | None:
        if page := await db.fetch_one(delete(DBPage).where(DBPage.id == id).returning(DBPage)):
            return cls(**page)

    @classmethod
    async def archive(cls, id: int, user: User, archive: bool) -> Page | None:
        if page := await db.fetch_one(
            update(DBPage).values(active=not archive).where(DBPage.id == id).returning(DBPage)
        ):
            return cls(**page)

    @classmethod
    async def get_all(cls, author: User) -> list[Page]:
        """Return a list of all pages created by a user"""
        query = select(DBPage).where(DBPage.author == author.id)
        return [cls(**u) for u in await db.fetch_all(query)]


BlockId = constr(max_length=10)
BlockType = constr(max_length=16)


class BlockCreation(BaseModel):
    type: BlockType
    data: dict


class BlockUpdate(BaseModel):
    type: BlockType | None
    data: dict | None


class Block(BaseModel):
    id: BlockId
    page_id: int
    type: BlockType
    data: dict
    sequence: int

    @classmethod
    async def get(cls, page_id: int, id_: BlockId) -> Block | None:
        """Get a single block from the database."""
        if block := await db.fetch_one(select(DBBlock).where(DBBlock.page_id == page_id, DBBlock.id == id_)):
            return cls(**block)

    @classmethod
    @db.transaction()
    async def delete(cls, page_id: int, block_id: BlockId) -> Block | None:
        """Delete a single block from the database."""
        if block := await db.fetch_one(
            delete(DBBlock).where(DBBlock.page_id == page_id, DBBlock.id == block_id).returning(DBBlock)
        ):
            block = cls(**block)
            await db.execute(
                update(DBBlock)
                .values(sequence=DBBlock.sequence - 1)
                .where(DBBlock.page_id == page_id, DBBlock.sequence > block.sequence)
            )
            return block

    @classmethod
    async def get_slice(cls, page_id: int, from_: BlockId | None, size: int = 25) -> list[Block]:
        """Return a range of blocks for a given page. To get the next range of blocks, call it with the last block's id."""
        if from_ is None:
            query = select(DBBlock).where(DBBlock.page_id == page_id)
        else:
            start = aliased(DBBlock)
            query = (
                select(DBBlock)
                .join(start, start.page_id == DBBlock.page_id)
                .where(
                    start.id == from_,
                    start.page_id == page_id,
                    DBBlock.sequence > start.sequence,
                )
            )

        return [cls(**b) for b in await db.fetch_all(query.order_by(DBBlock.sequence).limit(size))]

    @classmethod
    @db.transaction()
    async def add(cls, page_id: int, block_id: BlockId, data: BlockCreation, sequence: int = None) -> Block:
        """
        Add a block to the page. Append it to the end if no sequence number is given.
        Otherwise, it will insert the block in the page and increment the sequence of all subsequent blocks.
        """
        if sequence is None:
            one = literal_column("1")
            sequence = select(func.count(one)).select_from(DBBlock).where(DBBlock.page_id == page_id).as_scalar()
        else:
            await db.execute(
                update(DBBlock)
                .values(sequence=DBBlock.sequence + 1)
                .where(DBBlock.page_id == page_id, DBBlock.sequence <= sequence)
            )

        return cls(
            **await db.fetch_one(
                insert(DBBlock)
                .values(page_id=page_id, id=block_id, sequence=sequence, **data.dict())
                .returning(DBBlock)
            )
        )

    @classmethod
    async def update(cls, page_id: int, block_id: BlockId, data: BlockUpdate) -> Block | None:
        """Update a block's type or data. To update the sequence, use `.swap` or `.move`."""
        if block := await db.fetch_one(
            update(DBBlock)
            .values(**data.dict(exclude_none=True))
            .where(DBBlock.id == block_id, DBBlock.page_id == page_id)
            .returning(DBBlock)
        ):
            return cls(**block)

    @classmethod
    @db.transaction()
    async def swap(cls, page_id: int, block1: BlockId, block2: BlockId):
        """
        Swap two blocks position.
        Throws an error if one of the block does not exists.
        The same error is thrown if the two blocks are identicals.
        """
        rows = await db.fetch_all(
            select(DBBlock.id, DBBlock.sequence).where(DBBlock.page_id == page_id, DBBlock.id in [block1, block2])
        )
        if len(rows) != 2:
            missing = {block1, block2} - {row["id"] for row in rows}
            raise ValueError(f"Unable to swap missing blocks: {missing}")

        rows[0]["sequence"], rows[1]["sequence"] = rows[1]["sequence"], rows[0]["sequence"]
        await db.execute_many(
            update(DBBlock)
            .values(sequence=bindparam("sequence"))
            .where(DBBlock.page_id == page_id, DBBlock.id == bindparam("id")),
            rows,
        )

    @classmethod
    @db.transaction()
    async def move(cls, page_id: int, block_id: BlockId, dst: int):
        """Move a block's position to anywhere. Will update sequence of other blocks."""
        src = await db.fetch_val(
            select(DBBlock.sequence).where(
                DBBlock.id == block_id,
                DBBlock.page_id == page_id,
            )
        )
        if dst == src:
            return

        direction = (src - dst) // abs(src - dst)
        await db.execute(
            update(DBBlock)
            .values(sequence=DBBlock.sequence + direction)
            .where(
                DBBlock.page_id == page_id,
                src < DBBlock.sequence if direction < 0 else dst <= DBBlock.sequence,
                src > DBBlock.sequence if direction > 0 else dst >= DBBlock.sequence,
            )
        )
        await db.execute(
            update(DBBlock)
            .values(sequence=dst)
            .where(
                DBBlock.page_id == page_id,
                DBBlock.id == block_id,
            )
        )
