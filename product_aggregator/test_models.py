import pytest


# test creating of a Product
# noinspection PyTestParametrized
@pytest.mark.django_db
@pytest.mark.parametrize("product__name", ["figurína kapitána Kirka"])
@pytest.mark.parametrize("product__description", ["Figurka Krirka s hlavou v dlaních v měřítku 1:14"])
def test_products(product):
    assert product.name == 'figurína kapitána Kirka'
    assert product.description == "Figurka Krirka s hlavou v dlaních v měřítku 1:14"


# test creating of a Product and bunch of Offers.
@pytest.mark.django_db
def test_offers(product_factory, offer_factory):
    offer_factory.reset_sequence(0)
    product = product_factory()
    offer = offer_factory(product=product)
    assert offer.product == product
    for x in range(10):
        offer_factory(product=product)
    offer = offer_factory(product=product)
    assert product.offers.count() == 12
    assert offer.price == 11
