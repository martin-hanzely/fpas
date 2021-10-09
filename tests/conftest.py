import asyncio
from typing import AsyncGenerator, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from fpas.db.session import async_engine, session_factory


@pytest.fixture(scope="session", autouse=True)
def migration() -> Generator[None, None, None]:
    import alembic.config

    alembic.config.main(argv=["upgrade", "head"])
    yield
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Redefined event_loop fixture for pytest-asyncio to support session scoped coroutines.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.connect() as connection:
        transaction = await connection.begin()
        session: AsyncSession = session_factory(bind=connection)
        await connection.begin_nested()

        yield session

        await session.close()
        await transaction.rollback()


@pytest.fixture
def app() -> FastAPI:
    from fpas.api.deps import get_db as get_db_dependency
    from fpas.main import get_app

    app = get_app()
    app.dependency_overrides[get_db_dependency] = get_db.__wrapped__  # use unwrapped get_db fixture
    return app


@pytest.fixture
async def initialized_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=initialized_app, base_url="http://testserver") as client:
        yield client
