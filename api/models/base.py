import os
from typing import Literal

from databases import Database
from sqlalchemy import MetaData, select
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import ClauseElement, Executable
from sqlalchemy.sql.compiler import StrSQLCompiler

db = Database(os.environ["DATABASE_URL"])
metadata = MetaData()
Base = declarative_base(metadata=metadata)
TempBase = declarative_base()


class create_table_as(Executable, ClauseElement):
    def __init__(
        self,
        table,
        select: select,
        temp: bool = False,
        on_commit: Literal["PRESERVE ROWS", "DELETE ROWS", "DROP"] | None = None,
    ) -> None:
        self.table = getattr(table, "__table__", table)
        self.select = select
        self.temp = temp
        self.on_commit = on_commit

    def _process_table(self, compiler: StrSQLCompiler, **kw):
        if isinstance(self.table, str):
            return self.table

        return compiler.process(self.table, asfrom=True, **kw)

    @property
    def _create_stmt(self):
        if self.temp:
            return "CREATE TEMP TABLE"

        return "CREATE TABLE"

    @property
    def _on_commit_stmt(self):
        if self.on_commit is None:
            return ""

        return f" ON COMMIT {self.on_commit}"


@compiles(create_table_as)
def _create_table_as(el: create_table_as, compiler: StrSQLCompiler, **kw):
    return "{el._create_stmt} {table}{el._on_commit_stmt} AS {query}".format(
        el=el,
        table=el._process_table(compiler, **kw),
        query=compiler.process(el.select, **kw),
    )
