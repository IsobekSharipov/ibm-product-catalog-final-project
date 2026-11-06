"""Basic API smoke tests using a temporary SQLite database."""

import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app


def test_product_lifecycle():
    """Create, list, update, check availability and delete a product."""
    with tempfile.TemporaryDirectory() as directory:
        engine = create_engine(f"sqlite:///{os.path.join(directory, 'test.db')}",
                               connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        session_factory = sessionmaker(bind=engine)

        def override_db():
            with session_factory() as session:
                yield session

        app.dependency_overrides[get_db] = override_db
        try:
            with TestClient(app) as client:
                response = client.post("/products", json={
                    "name": "Laptop", "category": "Electronics", "price": 899.99
                })
                assert response.status_code == 201
                product_id = response.json()["id"]
                assert len(client.get("/products?category=Electronics").json()) == 1
                assert client.patch(f"/products/{product_id}", json={"available": False}).status_code == 200
                assert client.get(f"/products/{product_id}/availability").json()["available"] is False
                assert client.delete(f"/products/{product_id}").status_code == 204
                assert client.get(f"/products/{product_id}").status_code == 404
        finally:
            app.dependency_overrides.clear()
            engine.dispose()
