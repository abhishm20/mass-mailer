# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import re

import dns.resolver


def validate_email(value):
    if not value:
        return True
    match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', value)
    return match


def verify_email(value):
    value = value.split('@')[1] if len(value.split('@')) > 1 else ''
    try:
        dns.resolver.query(value, 'MX')
    except:
        return False
    return True
