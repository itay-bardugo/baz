import pika


class RabbitMQClient:
    _DEFAULT_PORT = 5672

    def __init__(self):
        self._host = ""
        self._queue = ""
        self._port = ""
        self._connection = None

    def should_connect_to(self, host):
        self._host = host
        return self

    def on_default_port(self):
        self.on_port(__class__._DEFAULT_PORT)
        return self

    def on_port(self, port):
        self._port = port
        return self

    def establish_connection(self):
        _connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        return _connection
