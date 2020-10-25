from . import Repository
from timers.models import Timer


class TimerRepository(Repository):
    _model = Timer

    @classmethod
    def find_by_id(cls, obj_id) -> Timer:
        return super().find_by_id(obj_id)

    @classmethod
    def find_by_signature(cls, signature) -> Timer:
        return cls._model.objects.get(signature=signature)

    @classmethod
    def save(cls, model: Timer) -> Timer:
        return super().save(model)
