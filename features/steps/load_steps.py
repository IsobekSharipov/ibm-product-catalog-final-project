"""Behave steps for loading background product records."""

from behave import given
from sqlalchemy import delete

from app.database import Base, SessionLocal, engine
from app.models import Product


@given("the following products exist")
def step_load_products(context):
    """Load the products specified in the Gherkin background table."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        session.execute(delete(Product))

        for row in context.table:
            values = dict(zip(context.table.headings, row.cells))
            product = Product(
                name=values["name"],
                category=values["category"],
                description=values.get("description", ""),
                price=float(values["price"]),
                available=values.get("available", "true").lower()
                in ("true", "yes", "1"),
            )
            if values.get("id"):
                product.id = int(values["id"])
            session.add(product)

        session.commit()

    context.loaded_products = len(context.table)
