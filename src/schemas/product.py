from typing import Optional

from pydantic import BaseModel

from src.schemas.category import CategorySchema


class ProductSchema(BaseModel):
    id: str
    name: str
    category: CategorySchema
    description: Optional[str]
    price: int
