# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from datetime import datetime

from django.utils import timezone


def get_current_time(datetime_str=None):
    if datetime_str and len(datetime_str) == 10:
        timestamp = datetime.strptime(datetime_str[:10], "%Y-%m-%d")
    elif datetime_str:
        timestamp = datetime.strptime(datetime_str[:19], "%Y-%m-%dT%H:%M:%S")
    else:
        timestamp = timezone.now()
    return timestamp
