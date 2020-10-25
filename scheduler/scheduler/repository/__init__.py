from django.db.models import Model
from typing import Type


class Repository:
    _model: Type[Model] = None

    @classmethod
    def find_by_id(cls, obj_id):
        return cls._model.objects.get(pk=obj_id)

    @classmethod
    def save(cls, model: Model):
        return model.save()
