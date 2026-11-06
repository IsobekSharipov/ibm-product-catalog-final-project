"""FastAPI application entry point."""

from fastapi import FastAPI
from app.database import Base, engine
from app.routes.products import router as products_router
from app import models  # noqa: F401  Register SQLAlchemy models before create_all.

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Product Catalog API", version="0.1.0")
app.include_router(products_router)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
