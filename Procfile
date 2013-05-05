web: gunicorn -w 8 -t 30  wsgi
worker: python manage.py celery worker -B --loglevel=info
