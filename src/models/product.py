from typing import Optional

from sqlalchemy import ForeignKey, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Product(Base):
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="products")  # noqa
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    images_url: Mapped[list[str]] = mapped_column(ARRAY(String))
