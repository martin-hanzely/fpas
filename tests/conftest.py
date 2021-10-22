import asyncio
from asyncio.events import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncConnection

from fpas import crud
from fpas.models.item import Item
from fpas.db.session import async_engine, session_factory
from fpas.schemas.item import ItemCreate


@pytest.fixture(scope="session", autouse=True)
def migration() -> Generator[None, None, None]:
    import alembic.config

    alembic.config.main(argv=["upgrade", "head"])
    yield
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """
    Redefined event_loop fixture for pytest-asyncio to support session scoped coroutines.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_connection() -> AsyncGenerator[AsyncConnection, None]:
    """
    Common cached transaction for database session fixture and app dependency override.
    """
    async with async_engine.connect() as connection:
        transaction = await connection.begin()
        yield connection
        await transaction.rollback()


@pytest.fixture
async def get_db(db_connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = session_factory(bind=db_connection)
    yield session
    await session.close()


@pytest.fixture
def app(db_connection: AsyncConnection) -> FastAPI:
    from fpas.api.deps import get_db
    from fpas.main import get_app

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = session_factory(bind=db_connection)
        yield session
        await session.close()

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
async def initialized_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=initialized_app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
async def test_item(get_db: AsyncSession) -> Item:
    return await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))
