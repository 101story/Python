from celery import Celery
from celery_test.routing.celery_routing import celeryconfig

import asyncio

celery = Celery('tasks')
celery.config_from_object(celeryconfig)


async def worker(task, queue:str = 'quick_tasks'):
	for i in range(1, 10):
		print(f'{task} run: {i}')

		print(f'{task} \n {celery.control.inspect().scheduled()}')

		result = celery.send_task(
            f'celery_routing.{task}', args=[i], queue=queue)

		while result.state == 'PENDING':
			await asyncio.sleep(1)
		result = result.get()
		print(f'{task} run: {i} = {result}')


async def main():
	await asyncio.gather(
		worker('slow_task', 'slow_tasks'),
		worker('quick_task', 'quick_tasks'),
	)


if __name__ == '__main__':
	asyncio.run(main())


# {celery.control.inspect().active()}
# {'celery@VN-A02-220306.local': [
# 	{'id': '449ca5e2-6a76-4bc5-859b-c4104c9ac59c', 'name': 'celery_routing.slow_task', 'args': [6], 'kwargs': {}, 'type': 'celery_routing.slow_task', 'hostname': 'celery@VN-A02-220306.local', 'time_start': 1689238215.2219398, 'acknowledged': True, 'delivery_info': {'exchange': '', 'routing_key': 'slow_tasks', 'priority': 0, 'redelivered': None}, 'worker_pid': 28353},
# 	{'id': '938cfe3f-515a-407f-ba7d-6c3b30b4de9a', 'name': 'celery_routing.slow_task', 'args': [6], 'kwargs': {}, 'type': 'celery_routing.slow_task', 'hostname': 'celery@VN-A02-220306.local', 'time_start': 1689238209.759264, 'acknowledged': True, 'delivery_info': {'exchange': '', 'routing_key': 'slow_tasks', 'priority': 0, 'redelivered': None}, 'worker_pid': 28351},
# 	{'id': '76caadc7-6cb8-42b0-bf9a-6dc0405e0203', 'name': 'celery_routing.slow_task', 'args': [6], 'kwargs': {}, 'type': 'celery_routing.slow_task', 'hostname': 'celery@VN-A02-220306.local', 'time_start': 1689238213.1790397, 'acknowledged': True, 'delivery_info': {'exchange': '', 'routing_key': 'slow_tasks', 'priority': 0, 'redelivered': None}, 'worker_pid': 28352}
# 	]
# }