from django.urls import path

from core.views import *

urlpatterns = [
    path('email/mark_read', mark_read_email, name='mark-read-email'),
    path('email/mark_clicked', mark_email_clicked, name='mark-email-clicked'),
]
