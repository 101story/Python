
from celery import Celery
from proj.celeryconfig import celeryconfig

app = Celery('proj', include=['proj.tasks'])
app.config_from_object(celeryconfig)
# app = Celery(
#     'tasks',
#     broker='amqp://guest:guest@localhost:5672//',
#     backend='rpc://',
# )
# app = Celery(
#     'proj',
#     broker='amqp://guest:guest@localhost:5672//',
#     backend='redis://localhost:6379/1',
#     include=['proj.tasks']
# )

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

'''
# rabbitmq management
docker run --rm --hostname my-rabbit \
    -p 5672:5672 \
    -e RABBITMQ_DEFAULT_USER=guest \
    -e RABBITMQ_DEFAULT_PASS=guest \
    --name self-practice-rabbit \
    rabbitmq:3-management


    -p 8080:15672 \
'''

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
# celery -A tasks worker --loglevel=info
