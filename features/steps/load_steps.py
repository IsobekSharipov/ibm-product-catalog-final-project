"""Behave background steps that seed products through the REST API."""

import os

import requests
from behave import given


@given("the following products exist")
def step_load_products(context):
    """Create each product from the Gherkin table using POST /products."""
    base_url = getattr(
        context,
        "base_url",
        os.getenv("PRODUCT_API_URL", "http://127.0.0.1:8000"),
    ).rstrip("/")
    context.loaded_products = []

    for row in context.table:
        values = dict(zip(context.table.headings, row.cells))
        payload = {
            "name": values["name"],
            "category": values["category"],
            "description": values.get("description", ""),
            "price": float(values["price"]),
            "available": values.get("available", "true").strip().lower()
            in ("true", "yes", "1"),
        }

        response = requests.post(
            f"{base_url}/products",
            json=payload,
            timeout=10,
        )
        assert response.status_code == 201, (
            f"POST /products failed: {response.status_code} {response.text}"
        )
        context.loaded_products.append(response.json())

    assert len(context.loaded_products) == len(context.table.rows)
