import time

from ..offers import update_offers_for_products


def run():
    while True:
        update_offers_for_products()
        ttw = 60 - time.localtime()[5]
        time.sleep(ttw)
