import uuid


class Signature:
    @staticmethod
    def make():
        return uuid.uuid4().hex
