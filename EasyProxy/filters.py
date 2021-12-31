from abc import ABC, abstractmethod
from typing import Any, Iterable
from urllib.parse import urlencode


class InvalidValue(Exception):
    pass


def to_str(val: Any) -> str:
    return val if isinstance(val, str) else val.decode('UTF-8') if isinstance(val, bytes) else str(val)


def to_int(val: Any) -> int:
    if isinstance(val, int):
        return val
    int_val = int(val)
    return int_val if int_val == val else round(val)


class Filter(ABC):
    __slots__ = ('value', 'joins')

    @property
    @abstractmethod
    def key(self):
        pass

    @abstractmethod
    def value_validator(self, value):
        pass

    def __init__(self, value, joins: set = None):
        self.value = self.value_validator(value)
        joins = joins or set()
        joins.add(urlencode({self.key: self.value}))
        self.joins = joins

    def __and__(self, other):
        joins = self.joins | other.joins
        return type(self)(self.value, joins)

    def __str__(self) -> str:
        return '&'.join(self.joins)


class limitedValues(Filter, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def values(self):
        pass

    def invalid(self, value) -> InvalidValue:
        return InvalidValue(f'{repr(value)} not in {repr(self.values)}')


class limitedStringCaseInsensitive(limitedValues):
    __slots__ = ()

    def __or__(self, other: Filter):
        return type(self)(','.join(set(self.value.split(',')) | set(other.value.split(','))))

    def __ior__(self, other: Filter):
        self.value = (self | other).value
        return self

    def value_validator(self, value):
        values = []
        for i, value in enumerate(
                [el for el in (to_str(value).split(',') if isinstance(value, str) else value)]):
            if isinstance(value, int):
                value -= 1
                value = self.values[value]
            value = to_str(value).lower()
            if value not in self.values:
                raise self.invalid(value)
            values.append(value)
        return ','.join(values)


class Number(limitedValues):
    __slots__ = ()
    values = None

    def value_validator(self, value):
        try:
            value = to_int(value)
        except Exception as Error:
            raise self.invalid(value) from Error
        if self.values and value not in self.values:
            raise self.invalid(value)
        return value


class CC(Filter):
    __slots__ = ()

    def value_validator(self, value):
        values = [to_str(cc).strip() for cc in (value if isinstance(value, Iterable) else to_str(value).split(','))]
        return ','.join(values)


class Format(limitedStringCaseInsensitive):
    __slots__ = ()
    key = 'format'
    values = ('json', 'txt')


class Level(limitedStringCaseInsensitive):
    __slots__ = ()
    key = 'level'
    values = ('transparent', 'anonymous', 'elite')


class Type(limitedStringCaseInsensitive):
    __slots__ = ()
    key = 'type'
    values = ('http', 'https', 'socks4', 'socks5')


class LastCheck(Number):
    __slots__ = ()
    key = 'last_check'


class Port(Number):
    __slots__ = ()
    key = 'port'


class Ping(Number):
    __slots__ = ()
    key = 'ping'


class Limit(Number):
    __slots__ = ()
    key = 'limit'
    values = range(1, 21)


class Uptime(Number):
    __slots__ = ()
    key = 'uptime'
    values = range(1, 101)


class Country(CC):
    __slots__ = ()
    key = 'country'


class NotCountry(CC):
    __slots__ = ()
    key = 'not_country'


Last_Check = LastCheck
Not_Country = NotCountry

FormatJSON, FormatTXT = [Format(val) for val in Format.values]
TypeHTTP, TypeHTTPS, TypeSOCKS4, TypeSOCKS5 = [Type(val) for val in Type.values]
LevelTRANSPARENT, LevelANONYMOUS, LevelELITE = [Level(val) for val in Level.values]
TypeSOCKS = Type('socks4,socks5')
