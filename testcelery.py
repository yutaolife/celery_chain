# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'yutao'
__time__ = '2018/4/26 21:31'

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

from tasks.tasks import add,mul,reabc
from celery import chain
#res = add.apply_async((2, 2), link=mul.s(16))
res = chain(add.s(2,2),mul.s(16),reabc.s(1))()
print res.get()



