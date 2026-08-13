from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class BookImageCreate(BaseModel):
    image_url: str
    is_primary: int = 0


class BookImageOut(BaseModel):
    id: int
    image_url: str
    is_primary: int

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    price: Decimal
    discount_price: Decimal | None = None
    images: list[BookImageCreate] = []


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: Decimal | None = None
    discount_price: Decimal | None = None
    images: list[BookImageCreate] | None = None


class BookOut(BaseModel):
    id: int
    title: str
    category: str
    description: str | None
    price: Decimal
    discount_price: Decimal | None
    created_at: datetime | None
    updated_at: datetime | None
    images: list[BookImageOut] = []

    class Config:
        from_attributes = True


class BookList(BaseModel):
    total: int
    items: list[BookOut]