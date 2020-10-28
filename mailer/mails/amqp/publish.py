from mailer.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
import json


class Publish:
    _client = RabbitTaskQueueAdapter()

    @staticmethod
    def log(to, status):
        Publish. \
            _client.new_connection() \
            .set_queue("emails/log") \
            .publish(json.dumps({'to': to, 'status': status})).close_connection()
        Publish.report_bazinga(to, status)

    @staticmethod
    def send_email(email_address):
        Publish. \
            _client.new_connection() \
            .set_queue("emails/send") \
            .publish(json.dumps({'email-address': email_address})).close_connection()

    @staticmethod
    def report_bazinga(to, status):
        Publish. \
            _client.new_connection() \
            .set_queue("bazinga/report") \
            .publish(json.dumps({'to': to, 'status': status})).close_connection()
