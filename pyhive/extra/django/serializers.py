from .modifiers import foreign_key_id
from ...serializers import BaseSerializer
from ...modifiers import datetime_isoformat


class DjangoModelSerializer(BaseSerializer):
    default_modifiers = [datetime_isoformat, foreign_key_id]

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        initial_repr = {}

        for field in obj._meta.fields:
            initial_repr[field.name] = getattr(obj, field.name)

        return super(DjangoModelSerializer, self).serialize(obj, modifiers, initial_repr, *args, **kwargs)
