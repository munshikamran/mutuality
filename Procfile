web: gunicorn -w 8 wsgi
worker: python manage.py celery worker --loglevel=info
