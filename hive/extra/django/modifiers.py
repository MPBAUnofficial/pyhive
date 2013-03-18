from django.db.models import ForeignKey, OneToOneField


def foreign_key_id(obj, current, *args, **kwargs):
    for field in obj._meta.fields:
        if isinstance(field, (ForeignKey, OneToOneField)):
            if field.name in current:
                field_instance = current[field.name]
                if field_instance is not None and hasattr(field_instance, 'pk'):
                    current[field.name] = field_instance.pk
                else:
                    current[field.name] = None
    return current


