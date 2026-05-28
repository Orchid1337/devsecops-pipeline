from fastapi import APIRouter, HTTPException, status

from app.models import ItemCreate, ItemResponse

router = APIRouter(prefix="/api/v1/items", tags=["items"])

# In-memory store - swap for postgres/redis in a real deployment
_items_db: dict[int, ItemResponse] = {}
_next_id: int = 1


def _reset_db():
    """Wipe state between tests."""
    global _next_id
    _items_db.clear()
    _next_id = 1


@router.get("/", response_model=list[ItemResponse])
async def list_items():
    return list(_items_db.values())


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, owner_id: int = 1):
    global _next_id
    new_item = ItemResponse(id=_next_id, owner_id=owner_id, **item.model_dump())
    _items_db[_next_id] = new_item
    _next_id += 1
    return new_item


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    if item_id not in _items_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")
    return _items_db[item_id]


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in _items_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")

    existing = _items_db[item_id]
    updated = ItemResponse(id=item_id, owner_id=existing.owner_id, **item.model_dump())
    _items_db[item_id] = updated
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id not in _items_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")
    del _items_db[item_id]
