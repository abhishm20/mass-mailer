# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time

from settings import *


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        app_logger.info('%r - %2.2f sec' % (method.__name__, te - ts))
        return result
    return timed
