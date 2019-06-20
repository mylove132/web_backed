from celery import task, shared_task
import os
from api.models import *
from api.util.redis_cli import celery_redis

@shared_task()
def add(x,y):
    # return x + y
    print(x + y)
@shared_task()
def mul(x,y):
    print("%d * %d = %d" %(x,y,x*y))
    return x*y
@shared_task()
def sub(x,y):
    print("%d - %d = %d"%(x,y,x-y))
    return x - y
@task(ignore_result=True,max_retries=1,default_retry_delay=10)
def just_print():
    print("Print from celery task")

@task()
def exec_cmd(cmd,script_id,job_id,file_md5):
    with os.popen(cmd, 'r') as p:
        res = p.read()
        for line in res.splitlines():
            print(line)
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("chat_2202", {
                "type": "chat.message",
                "message": line,
            })
            if line.find('end of run') != -1:
                print('脚本执行完毕')
                result = celery_redis.get('celery-task-meta-{}'.format(job_id))
                history:{
                    "result":result
                }
                History.objects.create()

