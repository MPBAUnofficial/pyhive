from .utils import get_notnull
from .modifiers import public_fields, exclude_callables, generic_list


class SerializerType(type):
    def __new__(cls, name, parents, dct):
        add_to = dct.pop('add_to', None)
        serializer_for = dct.pop('serializer_for', None)
        class_intance = super(SerializerType, cls).__new__(cls, name, parents, dct)
        if add_to is not None and serializer_for is not None:
            add_to.add_serializer(class_intance, serializer_for)

        default_serializers = dct.pop('default_modifiers', [])
        setattr(class_intance, 'default_modifiers', default_serializers)

        return class_intance


class BaseSerializer(object):
    """
    A serializer is a object with a `serialize` method
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

    def __init__(self, custom_modifiers=None, *args, **kwargs):
        self.custom_modifiers = get_notnull(custom_modifiers, [])

    def add_custom_modifier(self, modifier):
        if modifier is not None:
            self.custom_modifiers.append(modifier)

    def apply_modifiers(self, obj, modifiers, initial_repr, *args, **kwargs):
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
            return initial_repr

        current_repr = initial_repr

        for mod_function in modifiers:
            current_repr = mod_function(obj, current_repr, *args, **kwargs)

        return current_repr

    def serialize(self, obj, modifiers=None, initial_repr=None, *args, **kwargs):
        if initial_repr is None:
            raise ValueError('initial_repr should not be None')

        final_modifiers = []
        if modifiers is None:
            modifiers = []

        if kwargs.pop('use_default_modifiers', True):
            final_modifiers.extend(self.default_modifiers)

        final_modifiers.extend(self.custom_modifiers)
        final_modifiers.extend(modifiers)

        return self.apply_modifiers(obj, final_modifiers, initial_repr, *args, **kwargs)


class GenericObjectSerializer(BaseSerializer):
    default_modifiers = [public_fields, exclude_callables]

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        initial_repr = vars(obj)
        return super(GenericObjectSerializer, self).serialize(obj, modifiers, initial_repr, *args, **kwargs)


class ListSerializer(BaseSerializer):
    default_modifiers = [generic_list]

    def __init__(self, custom_modifiers=None, *args, **kwargs):
        self.item_serializer = kwargs.pop('item_serializer', None)
        if self.item_serializer is None:
            raise ValueError('can\'t serialize a list without `item_serializer`')

        super(ListSerializer, self).__init__(custom_modifiers, *args, **kwargs)

    def serialize(self, obj, modifiers=None, *args, **kwargs):
        initial_repr = obj
        super(ListSerializer, self).serialize(obj, modifiers, initial_repr, *args, item_serializer=self.item_serializer, **kwargs)
