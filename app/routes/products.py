"""Product catalog REST endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """Add a product to the catalog."""
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=list[ProductRead])
def list_products(name: str | None = None, category: str | None = None,
                  available: bool | None = None, db: Session = Depends(get_db)):
    """List and optionally filter products."""
    query = select(Product)
    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))
    if available is not None:
        query = query.where(Product.available == available)
    return db.scalars(query.order_by(Product.id)).all()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Read one product."""
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    """Partially update a product."""
    product = get_product(product_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Remove a product."""
    product = get_product(product_id, db)
    db.delete(product)
    db.commit()


@router.get("/{product_id}/availability")
def check_availability(product_id: int, db: Session = Depends(get_db)):
    """Return whether a product is available."""
    product = get_product(product_id, db)
    return {"product_id": product.id, "available": product.available}
