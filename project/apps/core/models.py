# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid

from django.db import models
from django.shortcuts import reverse

from core import utility
from core.config import DEFAULT_SENDER_EMAIL, HOST_NAME
from core.constant import EMAIL_EVENT_TYPES


# Customr Model just for testing
class Customer(models.Model):
    name = models.TextField(max_length=500)
    email = models.EmailField()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ('id',)

    def __repr__(self):
        return f"{Customer.__name__} <{self.name}, {self.email}>"

    @staticmethod
    def send_email_to_all():
        from core.serializers import EmailSerializer
        for customer in Customer.objects.all():
            d = {
                'to': customer.email,
                'subject': 'Campaign from Finhosts',
                'body': f'''
                    Hi {customer.name},
                    <br><br>
                    Hope you are doing fine.
                    <br><br>
                    <a href='EMAIL_CLICK_TRACKING' tagret='_blank'>Click here to see</a>
                '''
            }
            s = EmailSerializer(data=d)
            s.is_valid(True)
            s.save()


class Email(models.Model):
    created_at = models.DateTimeField(db_index=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    subject = models.TextField(max_length=500)
    body = models.TextField(null=True, blank=True, default='')

    sender = models.CharField(max_length=1000, blank=True, null=True, default=DEFAULT_SENDER_EMAIL)
    to = models.CharField(max_length=1000)
    cc = models.CharField(max_length=1000, blank=True, null=True, default='')
    reply_to = models.CharField(max_length=1000, blank=True, null=True, default='')

    is_sent = models.BooleanField(default=False)
    tracking_id = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(max_length=50, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ('-created_at',)

    def __repr__(self):
        return f"{Email.__name__} <{self.to}, {self.subject}>"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = utility.get_current_time()
        self.updated_at = utility.get_current_time()

        self.tracking_id = uuid.uuid4()
        self.body = self.body + Email.get_open_tracking_link(self.tracking_id)
        self.body = self.body.replace("EMAIL_CLICK_TRACKING", Email.get_click_tracking_link(self.tracking_id))
        self.reply_to = self.reply_to + ';' + self.sender if self.reply_to else self.sender
        super().save(*args, **kwargs)

    @staticmethod
    def get_open_tracking_link(tracking_id):
        return f'<br><br><img src="{HOST_NAME + str(reverse("core:mark-read-email"))}?eid={tracking_id}"' \
               f' height="0" alt="Finshots" width="0" border="0">'

    @staticmethod
    def get_click_tracking_link(tracking_id):
        return f'{HOST_NAME + str(reverse("core:mark-email-clicked"))}?eid={tracking_id}'


class EmailEvent(models.Model):
    created_at = models.DateTimeField(db_index=True, null=True, blank=True)
    email = models.ForeignKey(Email, related_name='events', related_query_name='event', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=False, blank=False, choices=EMAIL_EVENT_TYPES)

    class Meta:
        verbose_name = "Email Event"
        verbose_name_plural = "Email Events"
        ordering = ('-created_at',)

    def __repr__(self):
        return f"{EmailEvent.__name__} <{self.email}, {self.type}>"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = utility.get_current_time()
        self.updated_at = utility.get_current_time()
        super().save(*args, **kwargs)
