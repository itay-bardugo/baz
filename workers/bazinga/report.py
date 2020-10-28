from baz.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
import json
from customers.amqp.consumer import Consumer


def consume(ch, method, properties, body):
    payload = json.loads(body)
    Consumer.bazinga_report(payload["to"], payload["status"])


rabbitmq = RabbitTaskQueueAdapter()
rabbitmq.new_connection().set_queue("bazinga/report").consume(consume)
