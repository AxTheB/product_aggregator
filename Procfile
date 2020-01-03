release: python manage.py migrate
web: daphne product_aggregator_dj.asgi:application -v 3 --port $PORT --bind 0.0.0.0
web1: gunicorn product_aggregator_dj.wsgi --log-file -
