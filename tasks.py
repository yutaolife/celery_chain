# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'yutao'
__time__ = '2018/4/26 21:33'

import os
from celery import Celery

env = os.environ
app = Celery(
    'tasks',
    broker=env.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0'),
    backend=env.get('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')
)
app.conf.update(CELERY_ACCEPT_CONTENT = ['json','pickle'],
                   CELERY_TASK_SERIALIZER='json',
                   CELERY_RESULT_SERIALIZER='json')

@app.task(name='tasks.add')
def add(x, y):
    return x + y


@app.task(name='mul.add')
def mul(x, y):
    print "x: ",x
    print "y: ",y
    return x * y

@app.task(name='reabc.add')
def reabc(x, y):
    return x - y

