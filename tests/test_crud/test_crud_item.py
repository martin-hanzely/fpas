import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from fpas import crud
from fpas.schemas.item import ItemCreate, ItemUpdate


@pytest.mark.asyncio
async def test_create_item(get_db: AsyncSession) -> None:
    item_in = ItemCreate(name="Test Item")
    item = await crud.item.create(get_db, obj=item_in)
    assert hasattr(item, "id")
    assert item.name == item_in.name


@pytest.mark.asyncio
async def test_create_duplicate_item(get_db: AsyncSession) -> None:
    await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))
    with pytest.raises(IntegrityError):
        await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))


@pytest.mark.asyncio
async def test_read_one_item_by_id(get_db: AsyncSession) -> None:
    item_created = await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))
    item_read = await crud.item.read_one(get_db, id=item_created.id)
    assert item_read
    assert item_created.name == item_read.name


@pytest.mark.asyncio
async def test_read_nonexistent_by_id(get_db: AsyncSession) -> None:
    item_read = await crud.item.read_one(get_db, id=1)
    assert item_read is None


@pytest.mark.asyncio
async def test_read_items(get_db: AsyncSession) -> None:
    item_created = await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))
    items = await crud.item.read(get_db)
    assert len(items) == 1
    assert item_created.id in [i.id for i in items]

    item_created_2 = await crud.item.create(get_db, obj=ItemCreate(name="Test Item 2"))
    items = await crud.item.read(get_db)
    assert len(items) == 2
    assert item_created_2.id in [i.id for i in items]


@pytest.mark.asyncio
async def test_update_item(get_db: AsyncSession) -> None:
    item_created = await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))
    update_data = ItemUpdate(name="Test Item 2")
    await crud.item.update(get_db, id=item_created.id, obj=update_data)
    item_read = await crud.item.read_one(get_db, id=item_created.id)
    assert item_read
    assert update_data.name == item_read.name


@pytest.mark.asyncio
async def test_update_nonexistent(get_db: AsyncSession) -> None:
    with pytest.raises(NoResultFound):
        await crud.item.update(get_db, id=1, obj=ItemUpdate(name="Test Item"))


@pytest.mark.asyncio
async def test_delete_item(get_db: AsyncSession) -> None:
    item_created = await crud.item.create(get_db, obj=ItemCreate(name="Test Item"))
    items = await crud.item.read(get_db)
    assert len(items) == 1
    await crud.item.delete(get_db, id=item_created.id)
    items = await crud.item.read(get_db)
    assert len(items) == 0
