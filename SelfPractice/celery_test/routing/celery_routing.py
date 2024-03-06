from celery import Celery
from kombu import Queue

import time


class CeleryConfig:
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'

    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Asia/Seoul'
    enable_utc = True
    result_expires = 3600

    # 오작동 한 작업을 전용 대기열로 라우팅하는 설정
    task_routes = {
        'tasks.add': 'low-priority'
    }

    # 작업 속도를 제한하는 설정
    task_annotations = {
        'tasks.add': {'rate_limit': '10/m'}
    }
    celery_create_missing_queues = True


celeryconfig = CeleryConfig()


app = Celery('tasks')
app.config_from_object(celeryconfig)
app.conf.task_default_queue = 'default'
app.conf.task_queues = (
	Queue('slow_tasks', routing_key='slow.#'),
	Queue('quick_tasks', routing_key='quick.#'),
)


@app.task
def slow_task(x):
	time.sleep(x)
	return x


@app.task
def quick_task(x):
    return x


# $ celery -A celery_routing worker -Q slow_tasks --loglevel=debug --concurrency=3
# $ celery -A celery_routing worker -Q quick_tasks --loglevel=debug --concurrency=3