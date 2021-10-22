from typing import Any

import pytest

from fpas.db.utils import async_postgres_dsn


@pytest.mark.parametrize(
    "input,expected_output",
    [
        pytest.param(
            "postgresql://abc:def@localhost:5432/123",
            "postgresql+asyncpg://abc:def@localhost:5432/123",
            id="valid dsn scheme"
        ),
        pytest.param(
            "mysql://abc:def@localhost:5432/123",
            "postgresql+asyncpg://abc:def@localhost:5432/123",
            marks=pytest.mark.xfail,
            id="invalid dsn scheme"
        )
    ]
)
def test_async_postgres_dsn(input: str, expected_output: str) -> Any:
    async_postgres_dsn(input) == expected_output
