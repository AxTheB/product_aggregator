Product aggregator service
==========================
Microservice which allows to browse product catalog and keeps track of prices

Setting up
----------
Direct setup:
* Clone app
* cd product_aggregator
* make virtual env
* pip install -r reqs/prod.txt
* prepare some empty database
* run make-env.sh which copies env-example to .env and sets SECRET_KEY
* edit .env and set values (can be overriden from environment variable)
* run firstrun.sh which finishes setting app up
* run django by either:
     - devel server `./manage.py runserver`
     - asgi server from command line `daphne product_aggregator_dj.asgi:application`
* start the price updater task: `./manage.py runscript product_aggregator.scripts.price_updater`


Using the service
-----------------
API is built with _Django REST framework_ and uses content negotiation, to show json in web browser either add `Accept: application/json` header or append `.json` to the url. All uuids must be hyphenated, lowercase.

Writes to non-existing or read-only fields are silentnly discarded. 


### GET /products
List all products

Request: -  
Response: 200 OK
```json[
    {
        "id": "<uuid>",
        "name": <string>,
        "description": <string>
    }
]
```

### POST /products
Create new product. Registers product in the Offers microservice

Request:
```json
{
    "name": "Borg cube",
    "description": "Cube full of mighty, scary, ruthless cyborgs. Will not buy again"
}
```
Response:  
HTTP 201 Created
```json
{
    "id": "<uuid from the product agregator service>",
    "name": "Borg cube",
    "description": "Cube full of mighty, scary, ruthless cyborgs. Will not buy again"
}
```
HTTP 400 Bad Request
Returns either general error:
```html

{
    "detail": <message>
}
```
or field error(s):
```json
{
    "name": [
        "This field is required."
    ],
    "description": [
        "This field is required."
    ]
}
```

### GET /products/:uuid:
Get product detail

Request: -  
Response:  
200 OK
```json
{
    "id": "235f575d-1fad-4959-8d9c-8eae6aab23e4",
    "name": "Borg cube",
    "description": "Cube full of mighty, scary, ruthless cyborgs. Will not buy again"
}
```
404 Not Found  
Returns human-readable "Not found" page for malformed uuid. For well-formed but not existing uuid the response is
```json
{
    "detail": "Not found."
}
```

### POST /products/:uuid:
Update product info. Will not try to register the updated product.
Request and Response same as product creation

### DELETE /products/:uuid:
Delete product. Has no way to notify Offers service, but stops polling for price changes.

Request: -  
Response:  
204 No Content

### GET /products/:uuid:/prices
Request: -
Response:
200 OK
```json
{
    "prices": [1392,... , 2023],
    "change": 145.33045977011494
}
```