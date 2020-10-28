from mailer.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
from mails.models import Email
from mailer.helperes import redis
from mails.builder.mailer import MailBuilder

import pickle
from collections import deque
from mails.amqp.publish import Publish
from mails.service.mailer import MailerService


class Consumer:
    _client = RabbitTaskQueueAdapter()

    @staticmethod
    def log(to, status):
        log = Email()
        log.to = to
        log.status = status
        log.save()
        return True

    @staticmethod
    def start(signature):
        redis_client = redis.connect()
        try:
            queue = redis_client.get(signature)
            queue = deque(pickle.loads(queue))
            emails = queue.popleft()
            for email in emails:
                Publish.send_email(email)
            redis_client.set(signature, pickle.dumps(queue))
        except IndexError:
            # no items in queue
            ...

    @staticmethod
    def send(address):
        mail_builder = MailBuilder()
        email = mail_builder.create().address(address).get()
        email = MailerService.send(email)
        Publish.log(email.to, email.status)
