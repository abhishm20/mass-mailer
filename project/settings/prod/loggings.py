# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

LOGS_DIR = os.path.expanduser('~/logs/')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s %(funcName)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'logzioFormat': {
            'format': '{"additional_field": "value"}'
        }
    },
    'handlers': {
        'db': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': '30',
            'filename': os.path.join(LOGS_DIR, 'db.log'),
            'formatter': 'verbose'
        },
        'djangolog': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'djangolog.log'),
            'formatter': 'verbose'
        },
        'app_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'app_log.log'),
            'formatter': 'verbose'
        }

    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['db'],
        },
        'django': {
            'handlers': ['djangolog'],
            'level': 'INFO',
            'propagate': True,
        },
        'app_log': {
            'handlers': ['app_log'],
            'level': 'DEBUG'
        }
    }
}

import logging

app_logger = logging.getLogger('app_log')
