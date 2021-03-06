import uuid

import pytest
from django.conf import settings as django_settings
from pytest import raises

from . import offers
from .models import Token


@pytest.mark.django_db
def test_reuse_local_token():
    """reuse token in database"""
    tokenval = uuid.uuid4()
    Token.objects.create(value=tokenval, blocker=1)
    assert str(tokenval) == offers.get_auth_token()


@pytest.mark.django_db
def test_multi_local_token_f():
    """bail out if we try to save multiple tokens"""
    t1 = Token.objects.create(value=uuid.uuid4(), blocker=1)
    from django.db import IntegrityError
    with raises(IntegrityError):
        Token.objects.create(value=uuid.uuid4(), blocker=1)



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
