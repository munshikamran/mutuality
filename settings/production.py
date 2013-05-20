DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': '',                      # Or path to database file if using sqlite3.
    'USER': '',                      # Not used with sqlite3.
    'PASSWORD': '',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
URL = "www.mymutuality.com"
FACEBOOK_APP_ID = '475217095841801'
FACEBOOK_APP_SECRET = '1304979d3d82251c8dd383e179c30126'

# celery
BROKER_URL = 'amqp://jkpvdzam:z1KpG7P9PTX-eMvOevGJztyct2IiyIun@lemur.cloudamqp.com/jkpvdzam'
BROKER_POOL_LIMIT = None

