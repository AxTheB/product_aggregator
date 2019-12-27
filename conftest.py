import pytest
from pytest_factoryboy import register

from tests.factories import ProductFactory, OfferFactory

register(ProductFactory)
register(OfferFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
