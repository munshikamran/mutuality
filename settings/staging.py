DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dummy.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
 }
FACEBOOK_APP_ID = '503402936389228'
FACEBOOK_APP_SECRET = '00c92e60a39c18b6ead3f69dba7aa6f1'
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
URL = 'www.thawing-lowlands-3501.herokuapp.com'
