"""Request and response validation schemas."""

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Fields required to create a product."""
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    price: float = Field(ge=0)
    available: bool = True


class ProductUpdate(BaseModel):
    """Optional fields for partial updates."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: float | None = Field(default=None, ge=0)
    available: bool | None = None


class ProductRead(ProductCreate):
    """Product returned to API clients."""
    model_config = ConfigDict(from_attributes=True)
    id: int
