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
    """It should update an existing product through the REST API."""
    product = ProductFactory()
    db_session.add(product)
    db_session.commit()

    response = client.patch(
        f"/products/{product.id}",
        json={"name": "Updated Product", "price": 149.99, "available": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product.id
    assert data["name"] == "Updated Product"
    assert data["price"] == 149.99
    assert data["available"] is False

    db_session.refresh(product)
    assert product.name == "Updated Product"
    assert product.price == 149.99
    assert product.available is False
