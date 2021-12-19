

python3 manage.py makemigrations --no-input

python3 manage.py migrate --settings=config.settings.prod
python3 manage.py collectstatic --noinput


python3 manage.py loaddata fixtures/auth-dump.json

exec gunicorn config.wsgi:application -b 0.0.0.0:8000 --reload
