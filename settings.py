import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.realpath(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY', 'must-change-this-key-and-keep-it-secret')

DEBUG = os.getenv('DEBUG', False)

TEMPLATE_DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']  # Not for use in production, repeat: NEVER USE IN PROD!

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'rest_framework',
    'authentication',
    'base',
    'beaker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

AUTH_USER_MODEL = 'authentication.MBUser'

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', ]
USE_DEPRECATED_API = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', 'changeme')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', 'changeme')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'authentication.pipeline.create_user_meta',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# The dj_database_url module reads and parses
# the DATBASE_URL environment variable
# DATABASE_URL is automatically set on Heroku
DATABASES = {
    'default': dj_database_url.config()
}

CELERY_QUEUE = os.getenv('CELERY_QUEUE', 'EOD_TASKS')
CELERY_AWS_BROKER_URL = os.getenv('CELERY_AWS_BROKER_URL', 'sqs://AWS_KEY_VALUE_HERE:AWS_SECRET_VALUE_HERE@')

# Splunk Configs
SPLUNK_HOST = os.getenv('SPLUNK_HOST', 'splunk.example.com')
SPLUNK_PORT = os.getenv('SPLUNK_PORT', '8089')
SPLUNK_USERNAME = os.getenv('SPLUNK_USERNAME', 'admin')
SPLUNK_PASSWORD = os.getenv('SPLUNK_PASSWORD', 'changeme')
SPLUNK_INDEX = os.getenv('SPLUNK_INDEX', 'main')
SPLUNK_HOSTNAME = os.getenv('SPLUNK_HOSTNAME', 'beaker.mailbeaker.dev')
SPLUNK_VERIFY = os.getenv('SPLUNK_VERIFY', 'True')
SPLUNK_VERIFY = False if SPLUNK_VERIFY == 'False' else True

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(created)f %(exc_info)s %(filename)s %(funcName)s %(levelname)s %(levelno)s %(lineno)d %(module)s %(message)s %(pathname)s %(process)s %(processName)s %(relativeCreated)d %(thread)s %(threadName)s'
        },
        'verbose': {
            'format': 'levelname=%(levelname)s asctime=%(asctime)s module=%(module)s process=%(process)d thread=%(thread)d message="%(message)s"'
        }
    },
    'handlers': {
        'splunk': {
            'level': LOG_LEVEL,
            'class': 'splunk_handler.SplunkHandler',
            'formatter': 'json',
            'host': SPLUNK_HOST,
            'port': SPLUNK_PORT,
            'username': SPLUNK_USERNAME,
            'password': SPLUNK_PASSWORD,
            'index': SPLUNK_INDEX,
            'hostname': SPLUNK_HOSTNAME,
            'sourcetype': 'json',
            'verify': SPLUNK_VERIFY
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'splunk'],
            'level': LOG_LEVEL
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['null'],
            'propagate': True
        },
        'django.db.backends': {
            'level': 'ERROR',
            'propagate': True
        },
        'django.request': {
            'level': 'WARNING',
            'propagate': True
        },
        # https://docs.djangoproject.com/en/1.8/topics/logging/#django-security
        'django.security': {
            'propagate': True,
            'level': 'DEBUG'
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

ADMIN_GROUP_NAME = 'admin'
PLATFORM_GROUP_NAME = 'platform'
WEBAPP_GROUP_NAME = 'webapp'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect'
)

try:
    from settingslocal import *
except ImportError:
    pass
