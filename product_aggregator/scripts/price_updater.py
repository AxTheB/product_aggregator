import time

from ..offers import update_offers_for_products, get_auth_token


def run():
    get_auth_token()  # ensure we have auth token
    while True:
        update_offers_for_products()
        ttw = 60 - time.localtime()[5]
        time.sleep(ttw)
