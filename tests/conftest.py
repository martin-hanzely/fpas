import os
from typing import AsyncGenerator, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from fpas.db.base import Base
from fpas.db.utils import async_postgres_dsn


POSTGRES_TEST_DSN = os.getenv(
    "POSTGRES_TEST_DSN", default="postgresql://postgres:postgres@localhost:5432/fpas_test"
)


@pytest.fixture(scope="session", autouse=True)
def migration() -> Generator[None, None, None]:
    engine = create_engine(POSTGRES_TEST_DSN, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_engine = create_async_engine(async_postgres_dsn(POSTGRES_TEST_DSN), echo=True)
    session_factory = sessionmaker(class_=AsyncSession, autoflush=False, autocommit=False)

    connection = await async_engine.connect()
    trans = await connection.begin()
    session: AsyncSession = session_factory(bind=connection)
    await connection.begin_nested()

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()


@pytest.fixture
def app() -> FastAPI:
    from fpas.main import get_app

    app = get_app()
    return app


@pytest.fixture
async def initialized_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=initialized_app, base_url="http://testserver") as client:
        yield client
