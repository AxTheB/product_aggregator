import uuid

import pytest
from django.conf import settings as django_settings
from django.test import TestCase
from pytest import raises

from . import offers
from .models import Token


@pytest.mark.django_db
def test_reuse_local_token():
    """reuse token in database"""
    tokenval = uuid.uuid4()
    Token.objects.create(value=tokenval)
    assert str(tokenval) == offers.get_auth_token()


@pytest.mark.django_db
def test_multi_local_token_f():
    """bail out if we get more tokens"""
    Token.objects.create(value=uuid.uuid4())
    Token.objects.create(value=uuid.uuid4())
    assert Token.objects.count() == 2
    with raises(offers.OffersAuthException):
        offers.get_auth_token()


class GetTokenTest(TestCase):
    """Obtain token from the db"""

    def setUp(self):
        self.tokenval = uuid.uuid4()
        Token.objects.get_or_create(value=self.tokenval)


@pytest.mark.skipif(django_settings.OFFERS_TEST_URL is None, reason="OFFERS_TEST_URL not set up")
@pytest.mark.django_db
def test_remote(settings):
    """with empty database we should get new token"""
    settings.OFFERS_URL = settings.OFFERS_TEST_URL
    token = offers.get_auth_token()
    db_tokens = Token.objects.all()
    assert db_tokens.count() == 1
    assert str(db_tokens[0].value) == token


@pytest.mark.django_db
def test_remote_f(settings):
    """with empty database we want to get new token, but cannot reach auth so raise OffersAuthException"""
    settings.OFFERS_URL = 'http://localhost'
    with raises(offers.OffersAuthException):
        offers.get_auth_token()
