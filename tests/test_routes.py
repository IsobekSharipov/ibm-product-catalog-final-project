"""REST API route tests for the product catalog."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Product
from tests.factories import ProductFactory


@pytest.fixture
def db_session():
    """Create an isolated database session for each test."""
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


@pytest.fixture
def client(db_session):
    """Provide a client using the isolated test database."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_read_a_product(client, db_session):
    """It should read a product using the REST API."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()

    response = client.get(f"/products/{product.id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == product.id
    assert data["name"] == product.name
    assert data["category"] == product.category
    assert data["description"] == product.description
    assert data["price"] == product.price
    assert data["available"] == product.available

def test_update_a_product(client, db_session):
    """It should create a product with POST and update it with PUT."""
    product = ProductFactory()

    create_response = client.post(
        "/products",
        json={
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "available": product.available,
        },
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    updated_description = "Updated product description"

    update_response = client.put(
        f"/products/{product_id}",
        json={
            "name": product.name,
            "category": product.category,
            "description": updated_description,
            "price": product.price,
            "available": product.available,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()
    assert data["id"] == product_id
    assert data["description"] == updated_description

    saved_product = db_session.get(Product, product_id)
    assert saved_product is not None
    assert saved_product.description == updated_description


def test_delete_a_product(client, db_session):
    """It should delete a product through the REST API."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()
    product_id = product.id

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204
    assert db_session.get(Product, product_id) is None

    read_response = client.get(f"/products/{product_id}")
    assert read_response.status_code == 404

def test_list_all_products(client, db_session):
    """It should return all products through the REST API."""
    products = [ProductFactory() for _ in range(3)]
    db_session.add_all(products)
    db_session.commit()

    response = client.get("/products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert {item["id"] for item in data} == {product.id for product in products}

def test_list_products_by_name(client, db_session):
    """It should filter products by name through the REST API."""
    matching_product = ProductFactory(name="Wireless Mouse")
    other_product = ProductFactory(name="Mechanical Keyboard")
    db_session.add_all([matching_product, other_product])
    db_session.commit()

    response = client.get("/products", params={"name": "Wireless Mouse"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == matching_product.id
    assert data[0]["name"] == "Wireless Mouse"

def test_list_products_by_category(client, db_session):
    """It should list only products matching the requested category."""
    matching_product = ProductFactory(category="Electronics")
    other_product = ProductFactory(category="Books")
    db_session.add_all([matching_product, other_product])
    db_session.commit()

    response = client.get("/products", params={"category": "Electronics"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == matching_product.id
    assert data[0]["category"] == "Electronics"

def test_list_products_by_availability(client, db_session):
    """It should list only available products through the REST API."""
    available_product = ProductFactory(available=True)
    unavailable_product = ProductFactory(available=False)
    db_session.add_all([available_product, unavailable_product])
    db_session.commit()

    response = client.get("/products", params={"available": "true"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == available_product.id
    assert data[0]["available"] is True
