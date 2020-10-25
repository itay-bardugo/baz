from . import Repository
from ..models import Customer


class CustomerRepository(Repository):
    _model = Customer

    @classmethod
    def find_by_id(cls, obj_id) -> Customer:
        return super().find_by_id(obj_id)

    @classmethod
    def find_by_schedule_signature(cls, signature) -> Customer:
        return cls._model.objects.get(schedule_signature=signature)


