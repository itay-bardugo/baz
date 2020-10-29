from abc import ABCMeta, abstractmethod


class TaskQueue(metaclass=ABCMeta):
    @abstractmethod
    def set_queue(self, queue_name) -> 'TaskQueue':
        ...

    @abstractmethod
    def publish(self, payload) -> 'TaskQueue':
        ...

    @abstractmethod
    def consume(self, callback) -> 'TaskQueue':
        ...

    @abstractmethod
    def new_connection(self) -> 'TaskQueue':
        ...

    @abstractmethod
    def close_connection(self) -> 'TaskQueue':
        ...
