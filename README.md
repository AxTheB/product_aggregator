Product aggregator service
==========================
Microservice which allows to browse product catalog and keeps track of prices

Setting up
----------
Direct setup:
* Clone app
* make virtual env
* pip install -r reqs/prod.txt
* prepare some empty database
* run firstrun.sh
* edit .env and set values (can be overriden from environment variable)
* run django by either:
     - devel server `./manage.py runserver`
     - asgi server from command line `daphne product_aggregator_dj.asgi:application`
* start the price updater task: `./manage.py runscript product_aggregator.scripts.price_updater`
