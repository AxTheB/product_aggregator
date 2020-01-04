import requests
from django.conf import settings
from django.db import IntegrityError
from django.utils.timezone import now

from .models import Token, Product, Offer


class OffersServiceError(Exception):
    """base for all exceptions raised when communicating with Offers microservice"""


class OffersAuthException(OffersServiceError):
    """raises on auth errors"""
    pass


class OffersBadRequest(OffersServiceError):
    """raises on 400 error"""
    pass


def get_auth_token():
    """Gets auth token from database or from remote location
    raises AuthException if it can not get the remote token
    returns uuid-token
    """
    try:
        token = Token.objects.get(blocker=1)
        return str(token.value)
    except Token.DoesNotExist:
        if settings.OFFERS_URL is not None:  # get token from service
            auth_url = settings.OFFERS_URL + '/auth'
            # we want json response
            headers = {
                #    'Accept': 'application/json'
            }
            remote_token_request = requests.post(auth_url, data={}, headers=headers)
            if remote_token_request.status_code == 201:
                token = remote_token_request.json()['access_token']
                db_token = Token(value=token, unique=1)
                try:
                    db_token.save()
                except IntegrityError:
                    return get_auth_token()
                return token
    raise OffersAuthException('Unable to obtain token')


def register_product(product):
    """registers new product in the offers microservice"""
    data = {
        'id': product.id,
        'name': product.name,
        'description': product.description
    }
    headers = {}

    if settings.OFFERS_URL is not None:
        headers.update({'Bearer': get_auth_token()})
        register_product_url = settings.OFFERS_URL + '/products/register'
        register_product_request = requests.post(register_product_url, data=data, headers=headers)
        if register_product_request.ok:
            product.registered = now()

    else:
        # here we can check register_product_request.status_code and act on it.
        pass
    return product


def get_offers(product):
    """lists new offers for product and saves them to database"""
    if settings.OFFERS_URL is None:
        return False
    offers_url = settings.OFFERS_URL + '/products/{id}/offers'.format(id=product.id)

    headers = {
        #    'Accept': 'application/json',
        'Bearer': get_auth_token(),
    }
    offers_request = requests.get(offers_url, headers=headers)
    if offers_request.ok:
        for offer in offers_request.json():
            db_offer, created = Offer.objects.get_or_create(
                remote_id=offer['id'],
                product=product,
                defaults={
                    'price': offer['price'],
                    'items_in_stock': offer['items_in_stock']
                }
            )
            # I assume the offers in service are immutable. If not then save always and maybe update timestamp
            if created:
                db_offer.save()
        return True
    else:
        if not offers_request.ok:
            if offers_request.status_code == 400:
                raise OffersBadRequest(offers_request.json()['msg'])
            if offers_request.status_code == 401:
                raise OffersAuthException(offers_request.json()['msg'])
            # we hit 404
        return False


def update_offers_for_products():
    """Get new offers for all registered products"""

    products = Product.objects.exclude(registered=None)
    for product in products:
        get_offers(product)
