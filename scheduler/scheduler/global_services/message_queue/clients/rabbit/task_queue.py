from scheduler.global_services.message_queue.abstracts.task_queue import TaskQueue
from scheduler.global_services.message_queue.clients.rabbit.client import RabbitMQClient
import os
import pika


class RabbitTaskQueueAdapter(TaskQueue):

    def __init__(self):
        self._client = RabbitMQClient()
        self._connection = None
        self._channel = None
        self._queue_name = None

    def set_queue(self, queue_name) -> 'TaskQueue':
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue_name)
        self._queue_name = queue_name
        return self

    def publish(self, payload) -> 'TaskQueue':
        self._channel.basic_publish(exchange='', routing_key=self._queue_name, body=payload,
                                    properties=pika.BasicProperties(delivery_mode=2))

        return self

    def consume(self, callback) -> 'TaskQueue':
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=callback)
        self._channel.start_consuming()

        return self

    def new_connection(self) -> 'TaskQueue':
        self._connection = self._client.should_connect_to(
            os.environ.get("RABBIT-HOST")).on_default_port().establish_connection()
        return self

    def close_connection(self) -> 'TaskQueue':
        self._connection.close()
        return self
