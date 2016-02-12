
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db',
    }
}

DEBUG = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'changeme'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'changeme'


LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}
