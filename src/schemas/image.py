from pydantic import BaseModel


class ImageSchema(BaseModel):
    image_name: str
