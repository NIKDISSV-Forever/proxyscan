#### Documentation in Russian

> pip install [EasyProxies](https://pypi.org/project/EasyProxies/)

### См. также https://www.proxyscan.io/api

# Пример использования

_Напечатает до 20-и прокси ip:port каждый с новой строки:_

```python
from EasyProxies import *

my_filters = filters.TypeHTTP | filters.TypeHTTPS  # HTTP или HTTPS прокси
my_filters &= filters.Ping(10) & filters.Uptime(10)  # Пинг не больше 100 и Время безотказной работы 10%
print(*Proxies.get((my_filters & filters.Limit(20))), sep='\n')
```

_тоже самое что и_

```python
from EasyProxies import *

print(*Proxies.get(type='http,https', ping=10, uptime=10, limit=20), sep='\n')
```

```python
# __init__.py
from typing import Union
from EasyProxies import filters

__all__ = ('Proxies', 'filters')

ParamsType = dict[str, Union[str, int]]
ListOfProxy = list[Union[dict[str, Union[str, int, type(None)]], str]]
DEFAULT_FILTERS: filters.Parameters = filters.FormatTXT


class Proxies:
    HOST = 'https://www.proxyscan.io/'

    def __init__(self, default: filters.Parameters, host: str = HOST):
        """Задаёт фильтры по умолчанию, меняет хост"""
        ...

    @classmethod
    def raw_request(cls, params: Union[ParamsType, str]) -> ListOfProxy: ...

    @classmethod
    def get(cls, filters: Union[filters.Parameters, ParamsType, str] = DEFAULT_FILTERS) -> ListOfProxy: ...

    @classmethod
    def download_type(cls, protocol: filters.Type) -> list[str]:
        """Вернёт список готовых прокси"""
        ...

    @classmethod
    def generator(cls, *args, perpetual: bool = True, **kwargs) -> Iterator[ListOfProxy]:
        """
        Генератор прокси, если perpetual,
        то будет генерировать по заданным пораметрам вечно.
        """
        ...
```

# Фильтры

Пакет ```EasyProxy.filters```.

```python
from typing import TypeVar

_T = TypeVar('_T')


class Parameters:
    __slots__ = ('parameters',)

    def __init__(self, values=None): ...

    def __and__(self, other): ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...


class BaseParameter(Parameters):
    __slots__ = ('__key',)

    @property
    def key(self) -> str: ...

    def __init__(self, *values): ...

    def __or__(self, other): ...

    def valid_value(self, value: _T) -> set[_T]: ...


class LimitedValues(BaseParameter):
    off = False  # Игнорировать ограничения

    @property
    def values(self): ...

    def valid_value(self, value): ...


class Numbers(BaseParameter):
    def valid_value(self, value): ...


class CC:
    def __contains__(self, item) -> bool: ...  # in

    def __repr__(self) -> str: ...


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
```
