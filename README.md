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
DEFAULT_FILTERS: filters.Filter = filters.FormatTXT


class Proxies:
    HOST = 'https://www.proxyscan.io/'

    def __init__(self, default: filters.Filter, host: str = HOST):
        """Задаёт фильтры по умолчанию, меняет хост"""
        ...

    @classmethod
    def raw_request(cls, params: Union[ParamsType, str]) -> ListOfProxy: ...

    @classmethod
    def get(cls, filters: Union[filters.Filter, ParamsType, str] = DEFAULT_FILTERS) -> ListOfProxy: ...

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
from abc import ABC, abstractmethod
from typing import Any, Union


class Filter(ABC):
    __slots__ = ('value', 'as_dict')
    key = classmethod(property(...))

    @abstractmethod
    def value_validator(self, value): pass

    def __init__(self, *value, joins: dict = None): ...

    def __and__(self, other):  ...  # &

    def __bool__(self) -> bool: ...

    def __eq__(self, other) -> bool: ...

    def __str__(self) -> str: ...


class limitedValues(Filter):
    values = ...


class limitedStringCaseInsensitive(limitedValues):
    def __or__(self, other: limitedValues):  ...  # |


class Number(limitedValues):
    values = None

    def value_validator(self, value): ...


class CC(Filter): ...


class Format(limitedStringCaseInsensitive):
    values = ('json', 'txt')


class Level(limitedStringCaseInsensitive):
    values = ('transparent', 'anonymous', 'elite')


class Type(limitedStringCaseInsensitive):
    values = ('http', 'https', 'socks4', 'socks5')


class LastCheck(Number): ...


class Port(Number): ...


class Ping(Number): ...


class Limit(Number): values = range(1, 21)


class Uptime(Number): values = range(1, 101)


class Country(CC): ...


class NotCountry(CC): ...


ALL_FILTERS = [Format, Level, Type, LastCheck, Port, Ping, Limit, Uptime, Country, NotCountry]


def dict_to_filter(flt: Union[dict[str, Any], Filter] = None, **kwargs
                   ) -> Filter: ...


# Псевдонимы
Protocol = Type
Last_Check = LastCheck
Not_Country = NotCountry

FormatJSON, FormatTXT = ...
TypeHTTP, TypeHTTPS, TypeSOCKS4, TypeSOCKS5 = ...
LevelTRANSPARENT, LevelANONYMOUS, LevelELITE = ...
TypeSOCKS = Type('socks4', 'socks5')
```
