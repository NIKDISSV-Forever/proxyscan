from typing import Iterable, TypeVar
from urllib.parse import urlencode

_T = TypeVar('_T')


class InvalidValues(Exception):
    pass


def marge(a, b):
    return {**a, **b}


def _is_any_str(v) -> bool:
    return isinstance(v, (str, bytes))


class Parameters:
    __slots__ = ('parameters',)

    def __init__(self, values=None):
        self.parameters = values if values is not None else {}

    def __and__(self, other):
        return Parameters(marge(self.parameters, other.parameters))

    def __str__(self) -> str:
        return urlencode(
            {k: ','.join(str(i) for i in v) if not isinstance(v, (str, bytes)) and isinstance(v, Iterable) else v for
             k, v in
             self.parameters.items()})

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self.parameters)})'


class BaseParameter(Parameters):
    __slots__ = ('__key',)

    @property
    def key(self) -> str:
        if not hasattr(self, '__key'):
            self.__key = self.__class__.__name__.lower()
        return self.__key

    def __init__(self, *values):
        values = self.valid_value(values[0] if len(values) == 1 else set(values))
        super().__init__({self.key: values})

    def __or__(self, other):
        a = self.parameters
        b = other.parameters
        new = {}
        for k in set(a) & set(b):
            v1 = a[k]
            v2 = b[k]
            if _is_any_str(v1) or not isinstance(v1, Iterable):
                v1 = v1,
            if _is_any_str(v2) or not isinstance(v2, Iterable):
                v2 = v2,
            new[k] = {*v1, *v2}
        return Parameters(marge(marge(a, b), new))

    def valid_value(self, value: _T) -> set[_T]:
        if isinstance(value, Iterable):
            if _is_any_str(value):
                value = {value}
            elif not isinstance(value, set):
                value = set(value)
        else:
            value = {value}
        value = {val.lower() if _is_any_str(val) else val for val in value}
        return value


class LimitedValues(BaseParameter):
    off = False

    @property
    def values(self):
        self.off = True
        return ()

    def valid_value(self, value):
        values = self.values
        value = super().valid_value(value)
        if self.off:
            return value
        bad = {i for i in value if i not in values}
        good = value ^ bad
        if (not value) or bad:
            good = ', '.join(repr(i) for i in good)
            bad = ', '.join(repr(i) for i in bad)
            raise InvalidValues(
                f"{'Bad: ' if good else ''}{bad};{f' Good: {good};' if good else ''} For {repr(values)};")
        return value


class Numbers(BaseParameter):
    def valid_value(self, value):
        return {val if isinstance(val, int) else int(val) for val in super().valid_value(value)}


class CC:
    def __contains__(self, item) -> bool: return isinstance(item, str) and len(item) == 2

    def __repr__(self) -> str: return '<Country>'


class Format(LimitedValues):
    __slots__ = ()
    values = ('json', 'txt')


class Level(LimitedValues):
    __slots__ = ()
    values = ('transparent', 'anonymous', 'elite')


class Type(LimitedValues):
    __slots__ = ()
    values = ('http', 'https', 'socks4', 'socks5')


class Last_Check(Numbers):
    __slots__ = ()


class Port(Numbers):
    __slots__ = ()


class Ping(Numbers):
    __slots__ = ()


class Limit(Numbers):
    __slots__ = ()
    values = range(1, 21)


class Uptime(Numbers):
    __slots__ = ()
    values = range(1, 101)


class Country(LimitedValues):
    __slots__ = ()
    values = CC()


class Not_Country(Country):
    __slots__ = ()


Protocol = Type
LastCheck = Last_Check
NotCountry = Not_Country

FormatJSON, FormatTXT = [Format(val) for val in Format.values]
TypeHTTP, TypeHTTPS, TypeSOCKS4, TypeSOCKS5 = [Type(val) for val in Type.values]
LevelTRANSPARENT, LevelANONYMOUS, LevelELITE = [Level(val) for val in Level.values]
TypeSOCKS = Type({'socks4', 'socks5'})
