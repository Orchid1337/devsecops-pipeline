import re

from pydantic import BaseModel, Field, field_validator

# --- Health ---


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"


# --- Users ---


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=255)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v):
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("username")
    @classmethod
    def check_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, hyphens and underscores")
        return v


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int


# --- Items ---


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    price: float = Field(..., gt=0, le=1_000_000)

    @field_validator("name")
    @classmethod
    def strip_xss_chars(cls, v: str) -> str:
        # naive but effective for demo - strip obvious injection chars
        return re.sub(r"[<>\"';]", "", v).strip()


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    owner_id: int
