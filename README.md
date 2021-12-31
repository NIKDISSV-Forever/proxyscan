#### Documentation in Russian

> pip install [EasyProxies](https://pypi.org/project/EasyProxies/)

### См. также https://www.proxyscan.io/api

# Пример использования

_Напечатает до 20-и прокси ip:port каждый с новой строки:_

```python
from EasyProxies import *

my_filters = filters.TypeHTTP | filters.TypeHTTPS  # HTTP или HTTPS прокси
my_filters &= filters.Ping(10) & filters.Uptime(10)  # Пинг не больше 100 и Время безотказной работы 10%
print(*Proxies.get((my_filters & filters.FormatTXT & filters.Limit(20))), sep='\n')
```

```python
# __init__.py
from EasyProxies import filters

ParamsType = dict[str, Union[str, int]]
ProxyData = TypeVar('ProxyData', dict[str, Union[str, int, type(None)]], str)
ListOfProxy = list[ProxyData]
DEFAULT_FILTERS = filters.FormatTXT


class Proxies:
    HOST = 'https://www.proxyscan.io/'

    def __init__(self, default: filters.Filter):
        """Задаёт фильтры по умолчанию"""
        ...

    @classmethod
    def raw_request(cls, params: Union[ParamsType, str]) -> ListOfProxy: ...

    @classmethod
    def get(cls, filters: Union[filters.Filter, ParamsType, str] = DEFAULT_FILTERS) -> ListOfProxy: ...

    @classmethod
    def download_type(cls, protocol: filters.Type) -> list[str]:
        """Вернёт список готовых прокси"""
        ...
```

# Фильтры

Пакет ```EasyProxy.filters```.

```python

class Filter(ABC):
    key = ...

    @abstractmethod
    def value_validator(self, value): pass

    def __init__(self, value, joins: set = None): ...

    def __and__(self, other):  ...  # &

    def __str__(self) -> str: ...


class limitedValues(Filter):
    values = ...


class limitedStringCaseInsensitive(limitedValues):
    def __or__(self, other: limitedValues):  ...  # |

    def __ior__(self, other: limitedValues): ...  # |=


class Number(limitedValues):
    values = None
    ...


class CC(Filter): ...


class Format(limitedStringCaseInsensitive):
    values = ('json', 'txt')
    ...


class Level(limitedStringCaseInsensitive):
    values = ('transparent', 'anonymous', 'elite')
    ...


class Type(limitedStringCaseInsensitive):
    values = ('http', 'https', 'socks4', 'socks5')
    ...


class LastCheck(Number): ...


class Port(Number): ...


class Ping(Number): ...


class Limit(Number):
    values = range(1, 21)
    ...


class Uptime(Number):
    values = range(1, 101)
    ...


class Country(CC): ...


class NotCountry(CC): ...


# Псевдонимы
Last_Check = LastCheck
Not_Country = NotCountry

FormatJSON, FormatTXT = ...
TypeHTTP, TypeHTTPS, TypeSOCKS4, TypeSOCKS5 = ...
LevelTRANSPARENT, LevelANONYMOUS, LevelELITE = ...
TypeSOCKS = TypeSOCKS4 | TypeSOCKS5

```
