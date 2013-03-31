web: gunicorn -w 3 wsgi
worker: python manage.py celery worker --loglevel=info
