from django.db.models import ForeignKey, OneToOneField


def foreign_key_id(obj, current, *args, **kwargs):
    for field in obj._meta.fields:
        if isinstance(field, (ForeignKey, OneToOneField)):
            if field.name in current:
                current[field.name] = current[field.name].pk
    return current


