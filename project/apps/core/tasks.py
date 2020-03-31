# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from celery_config import celery_app
from core import email
from core.models import Email


@celery_app.task(name="send_email_task", queue="default_queue")
def send_email_task(email_data):
    message = {
        'subject': email_data['subject'],
        'body_html': email_data['body'],
        'is_attach_link': True if email_data['attachment_files'] else False
    }
    # Send email method call
    response = email.send_email(
        sender_name='Finshots', sender=email_data['sender'],
        recipients=email_data['to'].split(",") if email_data['to'] else [],
        cc=email_data['cc'].split(",") if email_data['cc'] else [], message=message
    )
    if response.status_code == 201:
        response = json.loads(response.content)
        data = dict()
        if 'id' in response:
            data['unique_id'] = response['id']
        if 'status' in response:
            data['status'] = response['status']
        data['is_sent'] = True
        Email.objects.filter(unique_id=email_data['unique_id']).update(**data)
