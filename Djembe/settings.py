# Django settings for Djembe project.
import os
from ConfigParser import RawConfigParser


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': './db.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

INTERNAL_IPS=('127.0.0.1',)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = RawConfigParser()
try:
	config.read(os.path.join(PROJECT_ROOT_PATH,'config.ini'))
except:
	config.read(os.path.join(PROJECT_ROOT_PATH,'config_blank.ini'))
EMAIL_HOST = config.get('email','EMAIL_HOST')
EMAIL_HOST_USER = config.get('email','EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('email','EMAIL_HOST_PASSWORD')
EMAIL_PORT = config.get('email','EMAIL_PORT')
EMAIL_USE_TLS = config.get('email','EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = 'djembe@cream.ly'
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH,"media")
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://shakazulu.cream.ly/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT_PATH,"static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r#bth$^$d(7c8+-7f0jf1hpfr$02g#-f0!k_3^wlx)%qoddp8h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'Djembe.login_required_middleware.LoginRequiredMiddleware',
    #'Djembe.stats_middleware.StatsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/$'

LOGIN_EXEMPT_URLS = (
    r'^accounts/invited',
    r'^accounts/register',
    r'^accounts/activate',
    r'^accounts/password',
    r'^static/',
    r'^tracker/',
    )

ROOT_URLCONF = 'Djembe.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Djembe.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH,"templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

AUTH_PROFILE_MODULE="userprofile.UserProfile"

PLUGINS = (

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'annoying',
    'plugins.music',
    'plugins.movies',
    'tags',
    'photo',
    'ajax',
    'registration',
    'invitation',
    'userprofile',
    'forum',
    'torrent',
    'tracker',
#    'ajax_select',
    #'djangobb_forum',
    #'haystack',
    #'messages',
    # Uncomment the next line to enable admin documentation:
    #'debug_toolbar',
     'django.contrib.admindocs',
)

ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_INVITATION_DAYS = 7
INVITATIONS_PER_USER = 5
INVITE_MODE = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'label'  : {'model':'plugins.music.models.Label', 'search_field':'name'}
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

MAX_SHOW_ALL_ALLOWED = 200

HAYSTACK_SITECONF = 'Djembe.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT_PATH, 'index')
"""HAYSTACK_CONNECTIONS = {
    'default': {
        'PATH':os.path.join(PROJECT_ROOT_PATH,'index'),
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100
    }
}"""

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
