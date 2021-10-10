import pytest

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from fpas.api.deps import get_item
from fpas.models.item import Item


@pytest.mark.asyncio
async def test_get_item(get_db: AsyncSession, test_item: Item) -> None:
    item = await get_item(get_db, item_id=test_item.id)
    assert item.name == test_item.name


@pytest.mark.asyncio
async def test_get_item_nonexistent(get_db: AsyncSession) -> None:
    with pytest.raises(HTTPException) as e:
        await get_item(get_db, item_id=1)
        assert e.status_code == HTTP_404_NOT_FOUND
