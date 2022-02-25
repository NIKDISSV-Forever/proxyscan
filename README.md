#### Documentation in Russian

> pip install [EasyProxies](https://pypi.org/project/EasyProxies/)

### См. также https://www.proxyscan.io/api

## Python

### Список из 20 прокси

```python
from EasyProxies import Proxies, const

print(*Proxies.get(limit=const.Limit(20), format=const.Format.TXT), sep='\n')
# Тоже что и
print(*Proxies.get(limit=20, format='txt'), sep='\n')
```

Если format='json' (по умолчанию), будет возвращён список из классов ProxyDescriptor

```python
@functools.total_ordering
class ProxyDescriptor(_AnyDescriptor):
    """A class for beautiful access to proxy attributes."""

    class Location(_AnyDescriptor):
        city: str
        continent: str
        country: str
        countryCode: str
        ipName: str
        ipType: str
        isp: str
        lat: str
        lon: str
        org: str
        query: str
        region: str
        status: str

    Ip: str
    Port: str
    Ping: int
    Time: int
    Type: list[str]
    Failed: bool
    Anonymity: str
    WorkingCount: int
    Uptime: float
    RecheckCount: int

    @property
    def as_requests_proxy(self) -> dict[str, str]:
        """
        Will result in a view for the proxy in the `requests` framework.
        {'http': host, 'https': host} if is_socks else {protocol: host}
        """
        ...

    def __str__(self):
        """Like format='txt'"""
        ...

    def __lt__(self, other: ProxyDescriptor) -> bool:
        """Designed for sorting"""
        ...
```


