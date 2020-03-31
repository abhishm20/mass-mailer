# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'lib.custom.paginations.NoPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
