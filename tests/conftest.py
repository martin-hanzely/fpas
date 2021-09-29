from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient


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
