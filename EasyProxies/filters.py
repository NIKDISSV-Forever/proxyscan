from abc import ABC, abstractmethod
from difflib import get_close_matches
from typing import Any, Iterable
from urllib.parse import urlencode


class InvalidValue(Exception):
    pass


def _to_str(val: Any) -> str:
    return val if isinstance(val, str) else val.decode('UTF-8') if isinstance(val, bytes) else str(val)


def _to_int(val: Any) -> int:
    if isinstance(val, int):
        return val
    int_val = int(val)
    return int_val if int_val == val else round(val)


class Filter(ABC):
    __slots__ = ('value', 'joins', '__key')

    @property
    def key(self):
        if not hasattr(self, '__key'):
            self.__key = self.__class__.__name__.lower()
        return self.__key

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


class limitedValues(Filter):
    __slots__ = ()

    @property
    @abstractmethod
    def values(self):
        pass

    def _invalid(self, value) -> InvalidValue:
        mb = ''
        if isinstance(value, Iterable):
            mb = get_close_matches(value, self.values, 1)
            if mb:
                mb = f' (Maybe you meant {repr(mb[0])}?)'
        return InvalidValue(f'{repr(value)} not in {repr(self.values)}{mb}')


class limitedStringCaseInsensitive(limitedValues):
    __slots__ = ()

    def __or__(self, other: limitedValues):
        return type(self)(set(self.value.split(',')) | set(other.value.split(',')))

    def value_validator(self, value):
        values = []
        for i, value in enumerate(_to_str(value).split(',') if isinstance(value, str) else value):
            if isinstance(value, int):
                value -= 1
                value = self.values[value]
            value = _to_str(value).lower()
            if value not in self.values:
                raise self._invalid(value)
            values.append(value)
        return ','.join(values)


class Number(limitedValues):
    __slots__ = ()
    values = None

    def value_validator(self, value):
        try:
            value = _to_int(value)
        except Exception as Error:
            raise self._invalid(value) from Error
        if self.values and value not in self.values:
            raise self._invalid(value)
        return value


class CC(Filter):
    __slots__ = ()

    def __init__(self, *value):
        super().__init__(value[0] if len(value) == 1 else value)

    def value_validator(self, value):
        values = [_to_str(cc).strip() for cc in (value.split(',') if isinstance(value, str) else value)]
        return ','.join(values)


class Format(limitedStringCaseInsensitive):
    __slots__ = ()
    values = ('json', 'txt')


class Level(limitedStringCaseInsensitive):
    __slots__ = ()
    values = ('transparent', 'anonymous', 'elite')


class Type(limitedStringCaseInsensitive):
    __slots__ = ()
    values = ('http', 'https', 'socks4', 'socks5')


class LastCheck(Number):
    __slots__ = ()
    key = 'last_check'


class Port(Number):
    __slots__ = ()


class Ping(Number):
    __slots__ = ()


class Limit(Number):
    __slots__ = ()
    values = range(1, 21)


class Uptime(Number):
    __slots__ = ()
    values = range(1, 101)


class Country(CC):
    __slots__ = ()


class NotCountry(CC):
    __slots__ = ()
    key = 'not_country'


Last_Check = LastCheck
Not_Country = NotCountry

FormatJSON, FormatTXT = [Format(val) for val in Format.values]
TypeHTTP, TypeHTTPS, TypeSOCKS4, TypeSOCKS5 = [Type(val) for val in Type.values]
LevelTRANSPARENT, LevelANONYMOUS, LevelELITE = [Level(val) for val in Level.values]
TypeSOCKS = TypeSOCKS4 | TypeSOCKS5
