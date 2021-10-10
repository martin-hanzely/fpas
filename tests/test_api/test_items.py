import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from fpas.models.item import Item
from fpas.schemas.item import ItemCreate, ItemUpdate


@pytest.mark.asyncio
async def test_create(client: AsyncClient) -> None:
    item_create = ItemCreate(name="Test Item")
    response = await client.post("/items/", json=jsonable_encoder(item_create, exclude_unset=True))
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == item_create.name
    assert "id" in item


@pytest.mark.filterwarnings("ignore:.*transaction already deassociated from connection")
@pytest.mark.asyncio
async def test_create_duplicate(client: AsyncClient, test_item: Item) -> None:
    item_create = ItemCreate(name=test_item.name)
    response = await client.post("/items/", json=jsonable_encoder(item_create, exclude_unset=True))
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_read(client: AsyncClient, test_item: Item) -> None:
    response = await client.get("/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert test_item.id in [f["id"] for f in items]


@pytest.mark.asyncio
async def test_read_one(client: AsyncClient, test_item: Item) -> None:
    response = await client.get(f"/items/{test_item.id}")
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == test_item.name


@pytest.mark.asyncio
async def test_read_nonexistent(client: AsyncClient) -> None:
    response = await client.get("/items/1")
    assert response.status_code == 404


# TODO
@pytest.mark.asyncio
async def test_update(client: AsyncClient, test_item: Item) -> None:
    item_update = ItemUpdate(name="Test Item 2")
    update_response = await client.put(
        f"/items/{test_item.id}", json=jsonable_encoder(item_update, exclude_unset=True)
    )
    assert update_response.status_code == 200
    response = await client.get(f"/items/{test_item.id}")
    item = response.json()
    assert item["name"] == item_update.name


# TODO
@pytest.mark.filterwarnings("ignore:.*transaction already deassociated from connection")
@pytest.mark.asyncio
async def test_update_duplicate(client: AsyncClient, test_item: Item) -> None:
    item_2 = ItemCreate(name="Test Item 2")
    response = await client.post("/items/", json=jsonable_encoder(item_2, exclude_unset=True))
    response = await client.put(
        f"/items/{test_item.id}",
        json=jsonable_encoder(ItemUpdate(name=item_2.name), exclude_unset=True)
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete(client: AsyncClient, test_item: Item) -> None:
    await client.delete(f"/items/{test_item.id}")
    response = await client.get("/items/")
    items = response.json()
    assert len(items) == 0


# TODO
@pytest.mark.asyncio
async def test_delete_nonexistent(client: AsyncClient) -> None:
    response = await client.delete("/items/1")
    assert response.status_code == 404
