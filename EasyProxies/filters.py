from abc import ABC, abstractmethod
from difflib import get_close_matches
from typing import Any, Iterable, TypeVar, Union
from urllib.parse import urlencode

_T = TypeVar('_T')


def _to_str(val: Any) -> str:
    return val if isinstance(val, str) else val.decode('UTF-8') if isinstance(val, bytes) else str(val)


def _to_int(val: Any) -> int:
    return val if isinstance(val, int) else int(val)


class InvalidValue(Exception):
    pass


class Filter(ABC):
    __slots__ = ('value', 'as_dict')

    @abstractmethod
    def value_validator(self, value):
        pass

    @classmethod
    @property
    def key(cls) -> str:
        if not hasattr(cls, '__key'):
            cls.__key = cls.__name__.lower()
        elif not cls.__key.islower():
            cls.__key = cls.__key.lower()
        return cls.__key

    def __init__(self, *value, joins: dict = None):
        value = value[0] if len(value) == 1 else value
        if joins is None:
            joins = {}
        self.value = self.value_validator(value)
        self.as_dict = joins | {self.key: self.value}

    def __and__(self: _T, other) -> _T:
        return type(self)(self.value, joins=other.as_dict)

    def __bool__(self) -> bool:
        return bool(self.as_dict)

    def __eq__(self, other) -> bool:
        return self.as_dict == other.as_dict

    def __str__(self) -> str:
        return urlencode(self.as_dict)


class limitedValues(Filter):
    __slots__ = ()

    @property
    @abstractmethod
    def values(self):
        pass

    def _invalid(self, value) -> InvalidValue:
        mb = not_in = ''
        if self.values:
            not_in = f' not in {repr(self.values)}'
            if isinstance(value, Iterable):
                mb = get_close_matches(value, self.values, 1)
                if mb:
                    mb = f' (Maybe you meant {repr(mb[0])}?)'
        return InvalidValue(f'{repr(value)}{not_in}{mb}')


class limitedStringCaseInsensitive(limitedValues):
    __slots__ = ()

    def __or__(self: _T, other: Filter) -> _T:
        return type(self)(set(self.value.split(',')) | set(other.value.split(',')))

    def value_validator(self, value):
        values = []
        enum_values = value
        if isinstance(value, str):
            enum_values = value.split(',')
        elif not isinstance(value, Iterable):
            enum_values = value,
        for i, value in enumerate(enum_values):
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
        value = _to_int(value)
        if self.values and value not in self.values:
            raise self._invalid(value)
        return value


class CC(Filter):
    __slots__ = ()

    def value_validator(self, value):
        return ','.join(_to_str(cc).strip() for cc in (value.split(',') if isinstance(value, str) else value))


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


ALL_FILTERS = [Format, Level, Type, LastCheck, Port, Ping, Limit, Uptime, Country, NotCountry]


def to_filter(flt: Union[dict[str, Any], Filter] = None, **kwargs) -> Filter:
    if flt is None:
        flt = {}
    if isinstance(flt, Filter):
        return flt & to_filter(kwargs)
    result = None
    flt |= kwargs
    for k, v in flt.items():
        for fl in ALL_FILTERS:
            if fl.key == k.lower():
                if result:
                    result &= fl(v)
                else:
                    result = fl(v)
    return result


Protocol = Type
Last_Check = LastCheck
Not_Country = NotCountry

FormatJSON, FormatTXT = [Format(val) for val in Format.values]
TypeHTTP, TypeHTTPS, TypeSOCKS4, TypeSOCKS5 = [Type(val) for val in Type.values]
LevelTRANSPARENT, LevelANONYMOUS, LevelELITE = [Level(val) for val in Level.values]
TypeSOCKS = Type('socks4', 'socks5')
