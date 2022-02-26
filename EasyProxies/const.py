from __future__ import annotations

import abc as _abc
import typing as _typing

_TV = _typing.TypeVar('_TV')
_TR = _typing.TypeVar('_TR')


class Safe(_abc.ABC):
    @classmethod
    @_abc.abstractmethod
    def _validator(cls, value: _TV, raises) -> _TR: pass

    def __new__(cls, values: _typing.Union[_TV, _typing.Iterable[_TV]], raises: bool = False
                ) -> _typing.Union[_TR, tuple[_TR]]:
        """
        If the raise True argument raises ValueError with an unsuitable value otherwise it returns DEFAULT or None
        """
        if not isinstance(values, str) and isinstance(values, _typing.Iterable):
            return tuple(cls._validator(value, raises) for value in values)
        return cls._validator(values, raises)


class SafeStr(Safe):
    __slots__ = ()
    ANY: tuple[str] = ()
    DEFAULT: str = None

    @classmethod
    def _validator(cls, value: _TV, raises) -> _typing.Optional[str]:
        if not isinstance(value, str): value = str(value)
        value = value.upper()
        allowed = tuple(el.upper() for el in cls.ANY)
        if value in allowed:
            return value
        elif raises:
            raise ValueError(f'{value!r} not in {allowed!r}')
        return cls.DEFAULT


class SafeRange(Safe):
    __slots__ = ()
    MIN: int = 1
    MAX: int

    @classmethod
    def _validator(cls, value: _TV, raises) -> int:
        allowed = range(cls.MIN, cls.MAX + 1)
        if value in allowed:
            return value
        elif raises:
            raise ValueError(f'{value!r} not in {allowed!r}')
        elif value > cls.MAX:
            return cls.MAX
        elif value < cls.MIN:
            return cls.MIN


class SafeCountryCode(Safe):
    __slots__ = ()

    @classmethod
    def _validator(cls, value, raises) -> _typing.Optional[str]:
        if not isinstance(value, str):
            value = str(value)
        if len(value) == 2:
            return value
        elif raises:
            raise ValueError(f'{value!r} is an invalid country code.')
        return


class AnyNumber(int): __slots__ = ()


class Format(SafeStr):
    """Format api output"""
    __slots__ = ()
    TXT = 'TXT'  # list[str]
    JSON = DEFAULT = 'JSON'  # list[ProxyDescriptor]
    ANY = (TXT, JSON)


class Level(SafeStr):
    """Anonymity Level"""
    __slots__ = ()
    TRANSPARENT = 'TRANSPARENT'
    ANONYMOUS = 'ANONYMOUS'
    ELITE = 'ELITE'
    ANY = DEFAULT = (ELITE, ANONYMOUS, TRANSPARENT)


class Type(SafeStr):
    """Proxy Protocol"""
    __slots__ = ()
    SOCKS4 = 'SOCKS4'
    SOCKS5 = 'SOCKS5'

    HTTP = 'HTTP'
    HTTPS = 'HTTPS'

    HTTPs = (HTTP, HTTPS)
    SOCKS = (SOCKS4, SOCKS5)

    ANY = DEFAULT = HTTPs + SOCKS


class LastCheck(AnyNumber):
    """Seconds the proxy was last checked"""
    __slots__ = ()


class Port(AnyNumber):
    """Proxies with a specific port"""
    __slots__ = ()


class Ping(AnyNumber):
    """How fast you get a response after you've sent out a request"""
    __slots__ = ()


class Limit(SafeRange):
    """How many proxies to list."""
    __slots__ = ()
    MIN = DEFAULT = 1
    MAX = 20


class Uptime(SafeRange):
    """How reliably a proxy has been running"""
    __slots__ = ()
    MIN = 1
    MAX = 100


class Country(SafeCountryCode):
    """Country of the proxy"""
    __slots__ = ()


class NotCountry(SafeCountryCode):
    """Avoid proxy countries"""
    __slots__ = ()
