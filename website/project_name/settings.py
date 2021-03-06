# Global settings for {{ project_name }} project.
import os
import sys

PROJECT_DIR = os.path.dirname(__file__)
WEBSITE_DIR = os.path.dirname(PROJECT_DIR)
PUBLIC_DIR = os.path.join(WEBSITE_DIR, 'public')

DEBUG = sys.platform == 'darwin'
TASTYPIE_FULL_DEBUG = DEBUG
TESTING = 'test' in sys.argv
TEMPLATE_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# the meta nginx.conf handles this for us.
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',
)
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '{{ project_name }}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    '{{ project_name }}.context_processors.processor',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'compressor',
    'django_nose',
    'django_jinja',
    'django_forms_bootstrap',
    'sorl.thumbnail',
    '{{ project_name }}',
)
if not (DEBUG or TESTING):
    INSTALLED_APPS += (
        'raven.contrib.django',
    )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SENTRY_DSN_PATH = os.path.join(WEBSITE_DIR, 'sentry.dsn')
if not os.path.exists(SENTRY_DSN_PATH):
    print "!!! WARNING SENTRY_DSN_PATH does not exist; no Sentry logging can occur !!!"
else:
    SENTRY_DSN = open(SENTRY_DSN_PATH).read().strip()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(WEBSITE_DIR, 'run', 'gunicorn.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, '{{ project_name }}.db'), # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:{0}/run/memcached.sock'.format(WEBSITE_DIR),
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{ secret_key }}'

JINJA2_EXTENSIONS = [
    'compressor.contrib.jinja2ext.CompressorExtension',
]
COMPRESS_ENABLED = True
COMPRESS_PARSER = 'compressor.parser.LxmlParser'
import jinja2
from django_forms_bootstrap.templatetags.bootstrap_tags import as_bootstrap, as_bootstrap_inline, as_bootstrap_horizontal
jinja2.filters.FILTERS['as_bootstrap'] = as_bootstrap
jinja2.filters.FILTERS['as_bootstrap_inline'] = as_bootstrap_inline
jinja2.filters.FILTERS['as_bootstrap_horizontal'] = as_bootstrap_horizontal

if DEBUG:
    # Show emails in the console during developement.
    DEFAULT_FROM_EMAIL = "mrooney@gmail.com"
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    DEFAULT_FROM_EMAIL = "mrooney@gmail.com"
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = True
    AWS_CREDENTIALS_PATH = os.path.join(WEBSITE_DIR, 'aws.credentials')
    if os.path.exists(AWS_CREDENTIALS_PATH):
        EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = open(AWS_CREDENTIALS_PATH).read().splitlines()


AUTH_USER_MODEL = "{{project_name}}.CustomUser"
LOGIN_URL = "login"

WEBSITE_NAME = "{{ project_name }}"
from settings_deploy import SERVICES
if DEBUG:
    WEBSITE_URL = "http://localhost:{}".format(SERVICES['nginx']['port'])
else:
    WEBSITE_URL = "http://example.com"

