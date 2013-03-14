def serializable(serializer):
    def inner(cls):
        def hive_serialize(self, modifiers=None, *args, **kwargs):
            return self.hive_serializer.serialize(self, modifiers, *args, **kwargs)

        setattr(cls, 'hive_serializer', serializer)
        setattr(cls, 'hive_serialize', hive_serialize)
        return cls
    return inner
