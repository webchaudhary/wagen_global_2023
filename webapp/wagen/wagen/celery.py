#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 15:40:11 2021

@author: lucadelu
"""

import os
import sys
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagen.settings')

app = Celery('wagen')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
