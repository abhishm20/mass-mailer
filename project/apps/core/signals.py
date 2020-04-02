# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.config import MAIL_ENABLED
from core.models import Email
from settings import app_logger


@receiver(post_save, sender=Email)
def send_email_post_signal(sender, instance, *args, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        if MAIL_ENABLED:
            from core.serializers import EmailSerializer
            email_data = EmailSerializer(instance).data
            app_logger.info({
                'type': "EMAIL-DATA",
                'data': email_data
            })
            from core.tasks import send_email_task
            send_email_task.delay(email_data)
