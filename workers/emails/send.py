from mailer.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
from mails.amqp.consumer import Consumer
import json


def consume(ch, method, properties, body):
    payload = json.loads(body)
    Consumer.send(payload['email-address'])


rabbitmq = RabbitTaskQueueAdapter()
rabbitmq.new_connection().set_queue("emails/send").consume(consume)
