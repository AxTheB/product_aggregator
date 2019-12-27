import random

import factory
from faker import Factory as FakerFactory

from product_aggregator.models import Product, Offer

faker = FakerFactory.create()
faker.seed_instance(12345)


class ProductFactory(factory.django.DjangoModelFactory):
    """Product factory."""
    name = factory.LazyAttribute(lambda x: faker.name())
    description = factory.LazyAttribute(lambda x: faker.sentence(nb_words=4))

    class Meta:
        model = Product


class OfferFactory(factory.django.DjangoModelFactory):
    """Offer factory."""
    price = factory.Sequence(int)
    # created = factory.Sequence(fake_time)
    items_in_stock = random.randint(1, 1000)
    remote_id = factory.Sequence(int)

    class Meta:
        model = Offer

    product = factory.SubFactory(ProductFactory)
