import os

from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

db = Database(os.environ["DATABASE_URL"])
metadata = MetaData()
Base = declarative_base(metadata=metadata)
