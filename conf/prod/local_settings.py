# -*- coding: utf-8 -*-

import raven
import os

DEBUG = False

SITE_ID = 1
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['gomachlearning.cloudapp.net']

MODELS_PATH = '/home/azureuser/Gosocket_project/models/'
CSV_PATH = '/home/azureuser/Gosocket_project/CSV/models_trained_test.csv'

RAVEN_CONFIG = {
    'dsn': 'https://aca622d180cc489fa0c47549aa259a2d:4f4f4ea90453459bbd6e1850f73bd15f@sentry.io/97703',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
