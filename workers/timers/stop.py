from scheduler.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
from scheduler.helperes import redis
from scheduler.repository.timer import TimerRepository
import json


def consume(ch, method, properties, body):
    payload = json.loads(body)
    if not (timer := TimerRepository.find_by_id(payload["timer-id"])):
        return False
    redis_client = redis.connect()
    redis_client.mset({timer.signature: 1})


rabbitmq = RabbitTaskQueueAdapter()
rabbitmq.new_connection().set_queue("timers/stop").consume(consume)
