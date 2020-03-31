# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/core/', include(('apps.core.urls', 'core'), namespace='core')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

admin.site.site_header = 'Mass Mailer Administration'
admin.site.site_url = "www.finshots.com"
