from ..models import Email
from random import randint


class MailerService:
    @staticmethod
    def send(email: Email):
        email.status = (email.FAILED, email.SUCCESSED)[randint(0, 1)]
        return email
