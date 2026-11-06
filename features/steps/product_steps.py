"""Behave steps for product read scenarios."""

from behave import then, when
from fastapi.testclient import TestClient

from app.main import app


@when("I request the product with ID {product_id:d}")
def step_read_product(context, product_id):
    """Request one product by ID."""
    with TestClient(app) as client:
        context.response = client.get(f"/products/{product_id}")


@then("the response status code should be {status_code:d}")
def step_check_status(context, status_code):
    """Verify HTTP response status."""
    assert context.response.status_code == status_code, context.response.text


@then('the product name should be "{name}"')
def step_check_name(context, name):
    """Verify the product name."""
    assert context.response.json()["name"] == name


@then('the product category should be "{category}"')
def step_check_category(context, category):
    """Verify the product category."""
    assert context.response.json()["category"] == category


@then("the product price should be {price:f}")
def step_check_price(context, price):
    """Verify the product price."""
    assert context.response.json()["price"] == price


@when('I update the product with ID {product_id:d} with name "{name}" and price {price:f}')
def step_update_product(context, product_id, name, price):
    """Update the product's name and price using the API."""
    with TestClient(app) as client:
        context.response = client.patch(
            f"/products/{product_id}",
            json={"name": name, "price": price},
        )


@when("I delete the product with ID {product_id:d}")
def step_delete_product(context, product_id):
    """Delete a product by ID using the API."""
    with TestClient(app) as client:
        context.response = client.delete(f"/products/{product_id}")
