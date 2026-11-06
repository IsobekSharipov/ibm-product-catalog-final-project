"""SQLAlchemy models."""

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Product(Base):
    """Product stored in the catalog."""

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String(1000), default="")
    price: Mapped[float] = mapped_column(Float)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
