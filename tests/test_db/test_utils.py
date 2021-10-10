import pytest

from fpas.db.utils import async_postgres_dsn


@pytest.mark.parametrize(
    "input,expected_output",
    [
        (
            "postgresql://abc:def@localhost:5432/123",
            "postgresql+asyncpg://abc:def@localhost:5432/123",
        ),
        pytest.param(
            "mysql://abc:def@localhost:5432/123",
            "postgresql+asyncpg://abc:def@localhost:5432/123",
            marks=pytest.mark.xfail,
            id="invalid dsn scheme"
        )
    ]
)
def test_async_postgres_dsn(input: str, expected_output: str):
    async_postgres_dsn(input) == expected_output
