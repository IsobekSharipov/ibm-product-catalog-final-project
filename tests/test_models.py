"""Unit tests for the Product database model."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Product
from tests.factories import ProductFactory


@pytest.fixture
def db_session():
    """Provide an isolated in-memory database for each test."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_read_a_product(db_session):
    """It should read a product from the database."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()

    saved_product = db_session.get(Product, product.id)

    assert saved_product is not None
    assert saved_product.id == product.id
    assert saved_product.name == product.name
    assert saved_product.category == product.category
    assert saved_product.description == product.description
    assert saved_product.price == product.price
    assert saved_product.available == product.available

def test_update_a_product(db_session):
    """It should update an existing product in the database."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()
    product_id = product.id

    product.name = "Updated Laptop"
    product.price = 1299.99
    product.available = False
    db_session.commit()
    db_session.expire_all()

    updated_product = db_session.get(Product, product_id)

    assert updated_product is not None
    assert updated_product.name == "Updated Laptop"
    assert updated_product.price == 1299.99
    assert updated_product.available is False

def test_delete_a_product(db_session):
    """It should delete a product from the database."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()
    product_id = product.id

    db_session.delete(product)
    db_session.commit()

    deleted_product = db_session.get(Product, product_id)

    assert deleted_product is None

def test_list_all_products(db_session):
    """It should list all products stored in the database."""
    products = [ProductFactory() for _ in range(5)]
    db_session.add_all(products)
    db_session.commit()

    saved_products = db_session.query(Product).all()

    assert len(saved_products) == 5
    assert {product.id for product in saved_products} == {
        product.id for product in products
    }
