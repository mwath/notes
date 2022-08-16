from __future__ import annotations

from datetime import datetime
from typing import Awaitable

from pydantic import BaseModel, constr
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
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

from .base import Base, TempBase, create_table_as, db
from .user import User

ONE = literal_column("1")
SEQUENCE_STEP = 256


class PageNotFound(Exception):
    def __init__(self, page: int):
        self.page = page
        super().__init__(f"Page id {page} does not exists.")


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
    __table_args__ = (UniqueConstraint("page_id", "sequence", deferrable=True),)

    id = Column(String(10), primary_key=True, nullable=False)
    page_id = Column(Integer, ForeignKey("pages.id"), primary_key=True, nullable=False)
    sequence = Column(Integer, nullable=False)
    type = Column(String(16), nullable=False)
    data = Column(JSONB, nullable=False)


class BlockFlatten(TempBase):
    __tablename__ = "block_flatten"

    id = Column(String(10), primary_key=True, nullable=False)
    seq = Column(Integer, nullable=False)


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
    def exists(cls, page_id: int) -> Awaitable[bool]:
        return db.fetch_val(select(true()).where(DBPage.id == page_id))

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

    @classmethod
    @db.transaction()
    async def _flatten(cls, page_id: int):
        # similar to enumerate(rows)
        seq = func.row_number().over(order_by=DBBlock.sequence) * SEQUENCE_STEP

        # Create a temporary table that holds the flattened sequences
        await db.execute(
            create_table_as(
                BlockFlatten,
                select(DBBlock.id.label("id"), seq.label("seq")).where(DBBlock.page_id == page_id),
                temp=True,
                on_commit="DROP",
            )
        )
        # Then update the sequences on the real table
        await db.execute(
            update(DBBlock)
            .values(sequence=BlockFlatten.seq)
            .where(DBBlock.page_id == page_id, DBBlock.id == BlockFlatten.id)
        )


BlockId = constr(max_length=10)
BlockType = constr(max_length=16)


class BlockCreation(BaseModel):
    type: BlockType
    data: dict
    before: BlockId | None = None


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
    async def delete(cls, page_id: int, block_id: BlockId) -> Block | None:
        """Delete a single block from the database."""
        if block := await db.fetch_one(
            delete(DBBlock).where(DBBlock.page_id == page_id, DBBlock.id == block_id).returning(DBBlock)
        ):
            return cls(**block)

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

        if size > 0:
            query = query.limit(size)

        return [cls(**b) for b in await db.fetch_all(query.order_by(DBBlock.sequence))]

    @classmethod
    async def add(cls, page_id: int, block_id: BlockId, data: BlockCreation) -> Block:
        """
        Add a block to the page. Append it to the end if no sequence number is given.
        Otherwise, it will insert the block in the page and increment the sequence of all subsequent blocks.
        """

        return await cls._insert(
            page_id,
            data.before,
            insert(DBBlock).returning(DBBlock),
            page_id=page_id,
            id=block_id,
            **data.dict(exclude={"before"}),
        )

    @classmethod
    async def _insert(cls, page_id: int, before: BlockId | None, query: insert | update, /, **kwargs) -> Block | None:
        if not await Page.exists(page_id):
            raise PageNotFound(page_id)

        if before is None:
            sequence = (
                select(SEQUENCE_STEP * (func.div(DBBlock.sequence, SEQUENCE_STEP) + 1))
                .where(DBBlock.page_id == page_id)
                .order_by(DBBlock.sequence.desc())
                .limit(1)
                .as_scalar()
            )
            block = await db.fetch_one(query.values(sequence=func.coalesce(sequence, 0), **kwargs))
        else:
            async with db.transaction():
                sequences: list[int] = [
                    s.sequence
                    for s in await db.fetch_all(
                        select(DBBlock.sequence)
                        .where(DBBlock.page_id == page_id, DBBlock.id <= before)
                        .order_by(DBBlock.sequence.desc())
                        .limit(2)
                    )
                ]

                if len(sequences) == 1:
                    sequence = SEQUENCE_STEP * (sequences[0] // SEQUENCE_STEP - 1)
                else:
                    bbseq, bseq = sequences
                    if abs(bseq - bbseq) <= 1:
                        await Page._flatten(page_id)
                    else:
                        sequence = (bseq + bbseq) // 2

                block = await db.fetch_one(query.values(sequence=sequence, **kwargs))

        if block:
            return cls(**block)

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
        await db.execute(
            """
        UPDATE blocks dst
            SET sequence = src.sequence
        FROM blocks src
        WHERE dst.page_id = :page_id
            AND src.page_id = :page_id
            AND dst.id IN (:block1, :block2)
            AND src.id IN (:block1, :block2)
            AND src.id != dst.id;""",
            {"page_id": page_id, "block1": block1, "block2": block2},
        )

    @classmethod
    @db.transaction()
    async def move(cls, page_id: int, block_id: BlockId, before: BlockId | None) -> Block | None:
        """Move a block's position to anywhere. Will update sequence of other blocks."""
        if block_id == before:
            return await cls.get(page_id, block_id)

        return await cls._insert(
            page_id,
            before,
            update(DBBlock).where(DBBlock.page_id == page_id, DBBlock.id == block_id).returning(DBBlock),
        )
