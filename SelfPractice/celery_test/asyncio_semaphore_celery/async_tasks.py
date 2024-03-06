import time
from celery import Celery


class CeleryConfig:
    # broker_url = 'amqp://guest:guest@localhost:5672//'
    broker_url = 'redis://localhost:6379/1'
    result_backend = 'redis://localhost:6379/2'

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


celeryconfig = CeleryConfig()

app = Celery('tasks', include=['async_tasks'])
app.config_from_object(celeryconfig)


@app.task
def xmax(numbers):
    time.sleep(1)
    return max(numbers)


@app.task
def xmin(numbers):
    time.sleep(2)
    return min(numbers)


@app.task
def xsum(numbers):
    time.sleep(5)
    return sum(numbers)


if __name__ == '__main__':
    app.start()

'''
# redis
docker pull redis:7.0.2-alpine

docker run --rm --hostname my-redis \
    -p 6379:6379 \
    --name self-practice-redis \
    redis:7.0.2-alpine

docker exec -it self-practice-redis redis-cli
> monitor
'''
# pip install -U "celery[redis]"
# celery -A async_tasks worker --loglevel=debug --concurrency=10
