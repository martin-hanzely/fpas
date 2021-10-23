# Fastapi plus Async SQLAlchemy example app

[![Tests](https://github.com/martin-hanzely/fpas/actions/workflows/main.yml/badge.svg)](https://github.com/martin-hanzely/fpas/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/martin-hanzely/fpas/branch/master/graph/badge.svg?token=Y3PW6IND8J)](https://codecov.io/gh/martin-hanzely/fpas)

This is a minimal FastAPI setup with SQLAlchemy ORM using its AsyncIO support included in version 1.4.

## The important parts


### Database connection

* Use `asyncpg` as connection driver in database URL.
* Use `create_async_engine` as engine factory.
* Specify `AsyncSession` as session class in session factory.

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker


ASYNC_POSTGRES_DSN = "postgresql+asyncpg://postgres:postgres@localhost:5432/db"

async_engine = create_async_engine(ASYNC_POSTGRES_DSN)

session_factory = sessionmaker(bind=async_engine, class_=AsyncSession)
```


### Database access

* ORM database access has to be awaited.

```python
from sqlalchemy.ext.asyncio import AsyncSession


async def create(db: AsyncSession) -> ModelType:
    db_obj = ModelClass()
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
```


### Testing using `pytest` framework with `pytest-asyncio` plugin

* The `event_loop` fixture provided by `pytest-asyncio` has to be redefined to use sesison scope.

```python
import asyncio
from asyncio.events import AbstractEventLoop
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

* Create `db_connection` fixture enclosed inside transaction. This is cached in function scope.

```python
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio.engine import AsyncConnection

from fpas.db.session import async_engine


@pytest.fixture
async def db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as connection:
        transaction = await connection.begin()
        yield connection
        await transaction.rollback()
```

* Use the `db_connection` fixture with session factory to create local session and dependency override.
* Both `get_db` fixture and `override_get_db` use the same database connection.


```python
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncConnection

from fpas.db.session import session_factory


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
```


## Documentation on the topic

* [FastAPI - Async SQL (Relational) Databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
* [SQLAlchemy 1.4. - AsyncIO Support](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
