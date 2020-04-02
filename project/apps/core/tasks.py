# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery_config import celery_app
from core import email
from core.models import Email, Customer


@celery_app.task(name="send_email_task", queue="default_queue")
def send_email_task(email_data):
    message = {
        'subject': email_data['subject'],
        'body_html': email_data['body']
    }
    # Send email method call
    d = {
        'sender_name': 'Finshots',
        'sender': email_data['sender'],
        'recipients': email_data['to'].split(",") if email_data['to'] else [],
        'message': message
    }
    d['recipients'] += email_data['cc'].split(",") if email_data['cc'] else []
    email.send_email(d)
    Email.objects.select_for_update().filter(tracking_id=email_data['tracking_id']).update(is_sent=True)


@celery_app.task(name="send_email_to_all_task", queue="default_queue")
def send_email_to_all_task():
    Customer.send_email_to_all()
