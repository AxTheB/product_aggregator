release: python manage.py migrate
web: daphne product_aggregator_dj.asgi:application -v 2 --port $PORT --bind 0.0.0.0
worker: python manage.py runscript product_aggregator.scripts.price_updater
