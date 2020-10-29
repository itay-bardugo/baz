from mailer.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
import json
from mails.amqp.consumer import Consumer


def consume(ch, method, properties, body):
    payload = json.loads(body)
    Consumer.log(payload["to"], payload["status"])


rabbitmq = RabbitTaskQueueAdapter()
rabbitmq.new_connection().set_queue("emails/log").consume(consume)
