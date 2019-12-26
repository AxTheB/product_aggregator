cp env-example .env
echo -n "SECRET_KEY=" >> .env
SECRET_KEY='none' ./manage.py generate_secret_key >> .env
