def serializable(serializer,
                 serializer_name='serializer',
                 serialize_method_name='serialize'):
    """
    Decorator that attaches an instance of a serializer to a class
    and also provides a serialize() method that serializes the instance
    upon wich it is called.
    >>> @serialize(GenericObjectSerializer(), serializer_name='serializer', serialize_method_name='serialize')
    >>> class A(object):
    >>>    def __init__(self):
    >>>       self.a = 11
    >>>       self.b = 22
    >>> A().serialize()
    {'a':11, 'b': 22}
    """

    def inner(cls):
        def serialize(self, modifiers=None, *args, **kwargs):
            serializer_object = getattr(self, serializer_name)
            return getattr(serializer_object, serialize_method_name)(self, modifiers, *args, **kwargs)

        serialize.__name__ = serialize_method_name

        setattr(cls, serializer_name, serializer)
        setattr(cls, serialize_method_name, serialize)
        return cls
    return inner
