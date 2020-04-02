# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from settings import DEBUG

DEFAULT_SENDER_EMAIL = "abhishek@loansimple.in"
HOST_NAME = "http://3.87.140.143"

if DEBUG:
    MAIL_ENABLED = True
else:
    MAIL_ENABLED = True
