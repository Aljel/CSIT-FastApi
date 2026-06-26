import os
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        self._db_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/csit_fastapi"
        )
        self._engine = create_engine(self._db_url)
        self._Session = sessionmaker(bind=self._engine)

    @contextmanager
    def session(self) -> Session:
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


database = Database()
Base = declarative_base()
