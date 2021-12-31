#### Documentation in Russian

> pip install [EasyProxies](https://pypi.org/project/EasyProxies/)

```python
# __init__.py
from EasyProxies import filters

ParamsType = dict[str, Union[str, int]]
ProxyData = TypeVar('ProxyData', dict[str, Union[str, int, type(None)]], str)
ListOfProxy = list[ProxyData]
DEFAULT_FILTERS = filters.FormatTXT


class Proxies:
    __slots__ = ()
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

Классовая обёртка для https://www.proxyscan.io/api

## Примеры фильтров

```python
from EasyProxies import *

my_filters = filters.TypeHTTP | filters.TypeHTTPS  # HTTP или HTTPS прокси
my_filters &= filters.Ping(10) & filters.Uptime(10)  # Пинг не больше 100 и Время безотказной работы 10%
print(*Proxies.get((my_filters & filters.FormatTXT & filters.Limit(20))), sep='\n')
"""
Напечатает до 20-и прокси ip:port каждый с новой строки
"""
```
