from .modifiers import mod_exclude_callables, mod_public_fields, mod_all_fields

class SerializerType(type):

    def __new__(cls, name, parents, dct):
        def get_and_del(key):
            tmp = dct.get(key, None)
            if key in dct:
                del dct[key]
            return tmp

        add_to, serializer_for = get_and_del('add_to'), get_and_del('serializer_for')
        instance = super(SerializerType, cls).__new__(cls, name, parents, dct)
        if add_to is not None and serializer_for is not None:
            add_to.add_serializer(instance, serializer_for)

        default_serializers = get_and_del('default_serializers')
        if default_serializers is not None:
            setattr(instance, 'default_serializers', default_serializers)

        return instance



class BaseSerializer(object):
    """
    A serializer is a object with a serialize method
    that takes an arbitrary object and converts it to a
    known representation suitable for serialization purposes.
    A known representation is almost always a combination of
    the python builtin types.
    Optionally the serialize method can take a modifiers list.
    A `modifier` is a python function that takes 4 arguments:
    - object: the object to be serialized
    - current: the current state of the serialization after applying the previous modifiers the .
    - *args, **kwargs: for future development
    """
    __metaclass__ = SerializerType

    def __init__(self, custom_serializers=None, *args, **kwargs):
        if custom_serializers is not None:
            



    def apply_modifiers(self, obj, modifiers, initial_repr=None, *args, **kwargs):
        """
        This function applies a list of modifiers to an object returning the appropriate
        representation of that object.
        It takes 5 parameters:
        - obj: the object to wich the modifier functions should be applied to.
        - modifiers: the list of modifiers to apply.
        - initial_repr: Is the initial state to wich the modifiers should be applied to.
        - *args, **kwargs: for future development
        """
        if not modifiers:
            return object

        current_repr = initial_repr

        for mod_function in modifiers:
            current_repr = mod_function(obj, current_repr)

        return current_repr

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        raise NotImplementedError('to be implemented in subclasses')


class GenericObjectSerializer(BaseSerializer):
    def __init__(self, custom_serializers=None, *args, **kwargs):
        self.default_modifiers = [mod_all_fields, mod_public_fields, mod_exclude_callables]
        if custom_serializers is None:
            custom_serializers = []

        self.custom_serializers = custom_serializers

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        if modifiers is None:
            modifiers = []
        return self.apply_modifiers(obj, self.default_modifiers + self.custom_serializers + modifiers, *args, **kwargs)
