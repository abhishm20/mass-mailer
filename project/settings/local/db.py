# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mass_mailer',
        'USER': 'root',
        'PASSWORD': 'Ainaa@007',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}
