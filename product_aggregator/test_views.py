import json
import uuid

import pytest
from django.conf import settings as django_settings
from django.urls import reverse

from . import offers
from .models import Product


# test product-list

@pytest.mark.django_db
def test_no_products(api_client):
    url = reverse('product_aggregator:product-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.django_db
def test_one_product(product, api_client):
    url = reverse('product_aggregator:product-list')
    response = api_client.get(url)
    assert response.status_code == 200
    content = json.loads(response.content)
    assert len(content) == 1
    assert content[0]['name'] == product.name
    assert content[0]['description'] == product.description


@pytest.mark.django_db
def test_product_create_locally(api_client, settings):
    settings.OFFERS_URL = None
    assert Product.objects.count() == 0
    data = {"name": "test name", "description": "test_description"}
    url = reverse('product_aggregator:product-list')
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert Product.objects.count() == 1
    content = json.loads(response.content)
    product = Product.objects.get(id=content['id'])
    assert product.name == content['name']


@pytest.mark.django_db
def test_product_create_locally(api_client, settings):
    settings.OFFERS_URL = None
    assert Product.objects.count() == 0
    data = {"name": "test name", "description": "test description"}
    url = reverse('product_aggregator:product-list')
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert Product.objects.count() == 1
    content = json.loads(response.content)
    product = Product.objects.get(id=content['id'])
    assert product.name == content['name']
    assert product.registered == None
    settings.OFFERS_URL = settings.OFFERS_TEST_URL
    assert offers.get_offers(product) == False


@pytest.mark.skipif(django_settings.OFFERS_TEST_URL is None, reason="OFFERS_TEST_URL not set up")
@pytest.mark.django_db
def test_product_create_register(api_client, settings):
    settings.OFFERS_URL = settings.OFFERS_TEST_URL
    data = {"name": "test name", "description": "test description"}
    url = reverse('product_aggregator:product-list')
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert Product.objects.count() == 1
    content = json.loads(response.content)
    product = Product.objects.get(id=content['id'])
    assert product.name == content['name']
    assert product.registered != None
    assert offers.get_offers(product) == True


# test product-detail


@pytest.mark.django_db
def test_one_product_detail(product, api_client):
    url = reverse('product_aggregator:product-detail', kwargs={'pk': product.pk})
    response = api_client.get(url)
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['name'] == product.name
    assert content['description'] == product.description


@pytest.mark.django_db
def test_one_product_detail_f(product, api_client):
    url = reverse('product_aggregator:product-detail', kwargs={'pk': uuid.uuid4()})
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_one_product_update(product, api_client):
    url = reverse('product_aggregator:product-detail', kwargs={'pk': product.pk})
    data = {
        'name': product.name + " updated",
        'description': product.description + " updated",
    }
    response = api_client.post(url, data=data)
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['name'] == data['name']
    assert content['description'] == data['description']


@pytest.mark.django_db
def test_one_product_delete(product, api_client):
    url = reverse('product_aggregator:product-detail', kwargs={'pk': product.pk})
    assert Product.objects.count() == 1
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_offers_for_one_product(product_factory, offer_factory, api_client):
    offer_factory.reset_sequence(1)
    product = product_factory()
    for x in range(10):
        offer_factory(product=product)
    url = reverse('product_aggregator:product-detail-prices', kwargs={'pk': product.pk})
    response = api_client.get(url)
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['prices'] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert content['change'] == 1000.0


@pytest.mark.django_db
def test_offers_for_one_product_limited(product_factory, offer_factory, api_client):
    offer_factory.reset_sequence(1)
    product = product_factory()
    times = []
    for x in range(10):
        o = offer_factory(product=product)
        times.append(o.created.isoformat())
    start = times[1]
    end = times[-2]
    url = reverse('product_aggregator:product-detail-prices', kwargs={'pk': product.pk})
    response = api_client.get(url, data={'from': start, 'to': end})
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['prices'] == [2, 3, 4, 5, 6, 7, 8, 9]
    assert content['change'] == 450.0
    response = api_client.get(url, data={'from': start})
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['prices'] == [2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert content['change'] == 500.0
