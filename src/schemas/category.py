from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: str
    name: str


class EditCategorySchema(BaseModel):
    name: str
