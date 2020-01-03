release: python manage.py migrate
web2: daphne product_aggregator_dj.asgi:application -v 3
web: gunicorn product_aggregator_dj.wsgi --log-file -
