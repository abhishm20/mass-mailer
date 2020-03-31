# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

from celery import Celery
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

celery_app = Celery('project')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.conf.task_default_queue = 'default_queue'
celery_app.conf.task_queues = (
    Queue('default_queue', routing_key='default_queue', consumer_arguments={'x-priority': 10}),
)

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()

# @celery_app.task(bind=True, name="testing")
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


celery_app.conf.beat_schedule = {

}
