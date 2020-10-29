from scheduler.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
from scheduler.repository.timer import TimerRepository
import json
from scheduler.classes.timer import StoppableTimer


def consume(ch, method, properties, body):
    payload = json.loads(body)
    if not (timer := TimerRepository.find_by_id(payload["timer-id"])):
        return False
    thread = StoppableTimer(timer.id)
    thread.start()


rabbitmq = RabbitTaskQueueAdapter()
rabbitmq.new_connection().set_queue("timers/add").consume(consume)
