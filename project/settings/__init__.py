from __future__ import absolute_import

from .base import *
from .drf import *

try:
    if os.environ.get('LSS_ENV') == 'prod':
        LSS_ENV = 'prod'
        from .prod import *
    else:
        LSS_ENV = 'local'
        from .local import *
except Exception as e:
    raise("Exception occured: ", e)
