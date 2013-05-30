# pyHive: Simple yet powerful obpject serialization #

## Introduction: ##
Hive can convert just about anything into basic python data structures that can later be converted into the format required (json, xml, ...).

## Basic usage (for plain old objects): ##
```python
>>> from pyhive.serializers import GenericObjectSerializer
>>> class A(object):
        def __init__(self):
            self.a = 22
            self.b = 44
>>> ser = GenericObjectSerializer()
>>> ser.serialize(A())
{'a': 22, 'b': 44}
```


## List serialization: ##
A list serializer works by applying a serializer instance to convert every single element of the list provided.
The item_serializer parameter is the instance to be used to serialize single elements of the list (it is required).

```python
>>> from pyhive.serializer import ListSerializer, GenericObjectSerializer
>>> class A(object):
        def __init__(self, n):
            self.n = n
>>> list_ser = ListSerializer(GenericObjectSerializer())
>>> list_ser.serialize([A(i) for i in range(3)])
[{'n': 0}, {'n': 1}, {'n': 2}]
```


## Django model serialization: ##
```python
>>> from pyhive.extra.django import DjangoModelSerializer
>>> from myproject import SomeModel
>>> ser = DjangoModelSerializer()
>>> ser.serialize(SomeModel.objects.get(pk=1))
```

## Modifiers ##
The most useful feature of pyhive are modifiers.
Modifiers are functions that alter the current representation of the object being converted.
The modifiers take 4 parameters:
1. obj: The object being converted
2. current: the current representation of the object (usually a dict)
3. *args, **kwargs: future usage
A modifier should return an altered version of current.
```python
>>> from pyhive.serializers import GenericObjectSerializer
>>> class A(object):
        def __init__(self):
            self.a = 22
            self.b = 44
>>> ser = GenericObjectSerializer()
>>> ser.serialize(A())
{'a': 22, 'b': 44}
>>> def mod(obj, current, *args, **kwargs):
        current['foo']='bar'
        return current
>>> ser.serialize(A(), modifiers=[mod])
{'a': 22, 'b': 44, 'foo': 'bar'}
```

