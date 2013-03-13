def mod_all_fields(obj, current, *args, **kwargs):
    return vars(obj)


def mod_public_fields(obj, current, *args, **kwargs):
    new = {}
    for k, v in current.items():
        if k.startswith('_'):
            continue
        new[k] = v
    return new


def mod_exclude_fields(exclude_list):
    def mod_exclude_fields(obj, current, *args, **kwargs):
        new = {}
        for k, v in current.items():
            if k in exclude_list:
                continue
            new[k] = v
        return new

    return mod_exclude_fields


def mod_exclude_callables(obj, current, *args, **kwargs):
    new = {}
    for k, v in current.items():
        if hasattr(v, '__call__'):
            continue
        new[k] = v
    return new
