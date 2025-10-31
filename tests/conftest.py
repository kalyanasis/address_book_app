import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

from app.db.base import Base
from app.db import session as session_mod
from app.main import app

@pytest.fixture(scope='session')
def engine():
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture()
def client(monkeypatch, engine):
    TestSessionLocal = sessionmaker(bind=engine)
    monkeypatch.setattr(session_mod, 'SessionLocal', TestSessionLocal)
    with TestClient(app) as c:
        yield c
