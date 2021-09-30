from fpas.crud.crud_base import CRUDBase
from fpas.models.item import Item
from fpas.schemas import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]): ...


item = CRUDItem(Item)
