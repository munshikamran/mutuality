DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mutuality',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
 }
FACEBOOK_APP_ID = '544374212239681'
FACEBOOK_APP_SECRET = 'e9609c52c461966845ff4ae6c186e458'
URL = "http://localhost:8000"

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
