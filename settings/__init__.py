import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

FORCE_SCRIPT_NAME = ""

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)

DEVELOPMENT_MODE = False
SHOULD_LOCKDOWN = False
ENVIRONMENT=os.environ.get('ENVIRONMENT')
if ENVIRONMENT:
    # determine if stage or prod
    print ENVIRONMENT
else:
    ENVIRONMENT = 'development'
    DEVELOPMENT_MODE = True


MANAGERS = ADMINS

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

#changed to be more universal... this will always give the absolute
#path for settings.py and everything is relative to it -- Jeff
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ABSOLUTE_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_MEDIA_PREFIX = '/admin/'


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
	ABSOLUTE_PATH
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
	# MUTUALITY RELATED APPLICATIONS
	'connect',
    'la_facebook',
    'messages',
    'rest_framework',
    'south',
    'djcelery'
)

try:
    import django_coverage
    INSTALLED_APPS += ('django_coverage',)
except ImportError:
    pass

AUTH_PROFILE_MODULE="connect.Profile"

LOGIN_REDIRECT_URL="/register/"

# password protection
if SHOULD_LOCKDOWN:
    INSTALLED_APPS += ('lockdown', )
    MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware', )
    LOCKDOWN_PASSWORD = 'Alpha-Tester'
    LOCKDOWN_FORM = 'lockdown.forms.LockdownForm'


# celery
import djcelery
djcelery.setup_loader()

# override and additional settings for different environments
from django.utils.importlib import import_module
import sys
def override_settings(dottedpath):
    try:
        _m = import_module(dottedpath)
    except ImportError:
        warnings.warn("Failed to import environment settings: %s" % dottedpath)
        pass
    else:
        _thismodule = sys.modules[__name__]
        for _k in dir(_m):
            if _k.isupper() and not _k.startswith('__'):
                setattr(_thismodule, _k, getattr(_m, _k))

override_settings('settings.%s' % ENVIRONMENT)

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

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'mutuality'
EMAIL_HOST_PASSWORD = 'myMutuality16'
EMAIL_PORT = 587
EMAIL_USE_TLS = True