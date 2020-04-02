# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import sys

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
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    },
    'loggers': {
        'app_log': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

import logging

app_logger = logging.getLogger('app_log')
