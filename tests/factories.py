"""Factories for generating realistic test products."""

import factory

from app.models import Product


class ProductFactory(factory.Factory):
    """Build fake Product instances for automated tests."""

    class Meta:
        model = Product

    id = factory.Sequence(lambda number: number + 1)
    name = factory.Faker("word")
    category = factory.Iterator(
        ["Electronics", "Books", "Home", "Clothing", "Sports"]
    )
    description = factory.Faker("sentence")
    price = factory.Faker(
        "pyfloat", left_digits=3, right_digits=2, positive=True, min_value=1
    )
    available = factory.Faker("boolean", chance_of_getting_true=80)
