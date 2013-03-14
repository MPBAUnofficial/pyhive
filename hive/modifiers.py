def public_fields(obj, current, *args, **kwargs):
    new = {}
    for k, v in current.items():
        if k.startswith('_'):
            continue
        new[k] = v
    return new


def exclude_fields(exclude_list):
    def mod_exclude_fields(obj, current, *args, **kwargs):
        new = {}
        for k, v in current.items():
            if k in exclude_list:
                continue
            new[k] = v
        return new

    return mod_exclude_fields


def exclude_callables(obj, current, *args, **kwargs):
    new = {}
    for k, v in current.items():
        if hasattr(v, '__call__'):
            continue
        new[k] = v
    return new


def generic_list(obj, current, *args, **kwargs):
    item_serializer = kwargs.pop('item_serializer')
    new = []
    for item in current:
        new.append(item_serializer.serialize(item))
    return new
