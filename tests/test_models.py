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
    """It should update a product description without changing its ID."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()

    original_id = product.id
    new_description = "Updated product description"

    product.description = new_description
    db_session.commit()
    db_session.expire_all()

    updated_product = db_session.get(Product, original_id)

    assert updated_product is not None
    assert updated_product.id == original_id
    assert updated_product.description == new_description

def test_delete_a_product(db_session):
    """It should delete a product and verify the database count."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()

    product_id = product.id

    assert db_session.query(Product).count() == 1

    db_session.delete(product)
    db_session.commit()

    assert db_session.query(Product).count() == 0

    deleted_product = db_session.get(Product, product_id)
    assert deleted_product is None

def test_list_all_products(db_session):
    """It should list all products stored in the database."""
    initial_products = db_session.query(Product).all()
    assert initial_products == []

    products = [ProductFactory() for _ in range(5)]
    db_session.add_all(products)
    db_session.commit()

    saved_products = db_session.query(Product).all()

    assert len(saved_products) == 5
    assert {product.id for product in saved_products} == {
        product.id for product in products
    }

def test_find_products_by_name(db_session):
    """It should find products matching a given name."""
    matching_product = ProductFactory(name="Wireless Mouse")
    other_product = ProductFactory(name="Mechanical Keyboard")
    db_session.add_all([matching_product, other_product])
    db_session.commit()

    results = db_session.query(Product).filter_by(name="Wireless Mouse").all()

    assert len(results) == 1
    assert results[0].id == matching_product.id
    assert results[0].name == "Wireless Mouse"

def test_find_products_by_category(db_session):
    """It should find only products in the requested category."""
    first = ProductFactory(category="Electronics")
    second = ProductFactory(category="Electronics")
    other = ProductFactory(category="Home")
    db_session.add_all([first, second, other])
    db_session.commit()

    results = db_session.query(Product).filter_by(category="Electronics").all()

    assert len(results) == 2
    assert {product.id for product in results} == {first.id, second.id}
    assert all(product.category == "Electronics" for product in results)

def test_find_products_by_availability(db_session):
    """It should find products matching the requested availability."""
    available_one = ProductFactory(available=True)
    available_two = ProductFactory(available=True)
    unavailable = ProductFactory(available=False)
    db_session.add_all([available_one, available_two, unavailable])
    db_session.commit()

    results = db_session.query(Product).filter_by(available=True).all()

    assert len(results) == 2
    assert {product.id for product in results} == {
        available_one.id, available_two.id
    }
    assert all(product.available is True for product in results)
