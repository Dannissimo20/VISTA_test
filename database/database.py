from contextlib import AbstractContextManager, contextmanager
from typing import ContextManager
import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("PG_DSN")
# engine: Engine = create_engine(DB_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class DBWriter:
    def __init__(self, dsn: str | None = None):
        self.engine = create_engine(dsn or DB_URL)

    def session(self) -> AbstractContextManager:
        return get_session(sessionmaker(self.engine))


@contextmanager  # type: ignore
def get_session(maker: sessionmaker[Session]) -> ContextManager[Session]:  # type: ignore
    with maker.begin() as session:
        try:
            yield session  # type: ignore
        except Exception as e:
            print(f"Session {maker} rollback: {e}")
            session.rollback()
            raise