from datetime import datetime, time
from ..serializers import BaseSerializer


def datetime_isoformat(obj, current, *args, **kwargs):
    new = {}
    for k, v in current.items():
        if issubclass(v.__class__, (time, datetime)):
            new[k] = v.isoformat()
        else:
            new[k] = v
    return new


class DjangoModelSerializer(BaseSerializer):
    default_modifiers = [datetime_isoformat]

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        initial_repr = {}

        for field in obj._meta.fields:
            initial_repr[field.name] = getattr(obj, field.name)

        return super(DjangoModelSerializer, self).serialize(obj, modifiers, initial_repr, *args, **kwargs)
