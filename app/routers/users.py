from fastapi import APIRouter, HTTPException, status

from app.models import UserCreate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["users"])

# Simple in-memory store. In prod this would be a real DB obviously.
_users_db: dict[int, UserResponse] = {}
_next_id: int = 1


def _reset_db():
    """Wipe state between tests."""
    global _next_id
    _users_db.clear()
    _next_id = 1


@router.get("/", response_model=list[UserResponse])
async def list_users():
    return list(_users_db.values())


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    global _next_id

    # Uniqueness check
    for existing in _users_db.values():
        if existing.username == user.username:
            raise HTTPException(
                status.HTTP_409_CONFLICT, f"Username '{user.username}' already taken"
            )
        if existing.email == user.email:
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    new_user = UserResponse(id=_next_id, **user.model_dump())
    _users_db[_next_id] = new_user
    _next_id += 1
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in _users_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User {user_id} not found")
    return _users_db[user_id]


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in _users_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User {user_id} not found")
    del _users_db[user_id]
