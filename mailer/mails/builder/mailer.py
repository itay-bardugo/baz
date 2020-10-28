from ..models import Email
from random import randint


class MailBuilder:
    __email: Email = None

    def create(self):
        MailBuilder.__email = Email()
        return self

    def address(self, address):
        MailBuilder.__email.to = address
        return self

    def get(self):
        return self.__email
