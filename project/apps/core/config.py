# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from settings import DEBUG

DEFAULT_SENDER_EMAIL = "help@loansimple.in"
HOST_NAME = "mailer.finshots.com"

if DEBUG:
    MAIL_ENABLED = True
else:
    MAIL_ENABLED = True
