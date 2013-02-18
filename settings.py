import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

FORCE_SCRIPT_NAME = ""

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)


DEVELOPMENT_MODE = False


MANAGERS = ADMINS

if DEVELOPMENT_MODE:
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
    FACEBOOK_APP_ID = '544374212239681'
    FACEBOOK_APP_SECRET = 'e9609c52c461966845ff4ae6c186e458'
    URL = "http://localhost:8000"
else:
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
    URL = "vast-thicket-3000.herokuapp.com"
    FACEBOOK_APP_ID = '475217095841801'
    FACEBOOK_APP_SECRET = '1304979d3d82251c8dd383e179c30126'

WSGI_APPLICATION = "Mutuality.wsgi.application"
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
# ADMIN_MEDIA_PREFIX = '/admin/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'static'),
)



# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hdik5*)66ahwns+q4ckb@7cehrq=n^e^^y23*sm(xn-f785b7b'
AUTH_PROFILE_MODULE = 'connect.Profile'

# AUTHENTICATION_BACKENDS = (
	# 'accounts.auth.EmailBackend',
	# 'django_facebook.auth_backends.FacebookBackend',
# )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	#'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), ''),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',
	'django.contrib.admindocs',
	# NEEYAA RELATED APPLICATIONS
	'connect',
    'la_facebook',
    'messages',
    'rest_framework',
    'south',
)

try:
    import django_coverage
    INSTALLED_APPS += ('django_coverage',)
except ImportError:
    pass

AUTH_PROFILE_MODULE="connect.Profile"

LOGIN_REDIRECT_URL="/register/"

FACEBOOK_ACCESS_SETTINGS = {
        "FACEBOOK_APP_ID": FACEBOOK_APP_ID,
        "FACEBOOK_APP_SECRET": FACEBOOK_APP_SECRET,
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "/tmp/la_facebook.log",
        # The following keys are optional
        # TODO - Comment next line out but still have tests pass
        "CALLBACK": "la_facebook.callbacks.default.default_facebook_callback", 
        "PROVIDER_SCOPE": ['email',\
        'user_location',\
        'friends_location',\
        'friends_relationship_details',\
        'friends_relationships',\
        'friends_birthday',\
        'friends_work_history',\
        'friends_education_history'], # FACEBOOK PERMISSIONS http://developers.facebook.com/docs/authentication/permissions/
}
