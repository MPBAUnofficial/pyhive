from django.db.models import ForeignKey, OneToOneField

from ...serializers import BaseSerializer
from ...modifiers import datetime_isoformat


def foreign_key_id(obj, current, *args, **kwargs):
    for field in obj._meta.fields:
        if isinstance(field, (ForeignKey, OneToOneField)):
            if field.name in current:
                current[field.name] = current[field.name].pk
    return current


class DjangoModelSerializer(BaseSerializer):
    default_modifiers = [datetime_isoformat, foreign_key_id]

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        initial_repr = {}

        for field in obj._meta.fields:
            initial_repr[field.name] = getattr(obj, field.name)

        return super(DjangoModelSerializer, self).serialize(obj, modifiers, initial_repr, *args, **kwargs)
