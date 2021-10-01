import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fpas import crud
from fpas.schemas.item import ItemCreate


@pytest.mark.asyncio
async def test_create_item(get_db: AsyncSession) -> None:
    item_in = ItemCreate(name="Test Item")
    item = await crud.item.create(get_db, obj=item_in)
    assert hasattr(item, "id")
    assert item.name == item_in.name


@pytest.mark.asyncio
async def test_read_one_item_by_id(get_db: AsyncSession) -> None:
    item_in = ItemCreate(name="Test Item")
    item_created = await crud.item.create(get_db, obj=item_in)
    item_read = await crud.item.read_one(get_db, id=item_created.id)
    assert item_read
    assert item_created.name == item_read.name
