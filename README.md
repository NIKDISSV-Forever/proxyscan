#### Documentation in Russian

> pip install [EasyProxies](https://pypi.org/project/EasyProxies/)

### См. также https://www.proxyscan.io/api

## Python

```python
class Proxies:
    """Interface for working with the proxyscan API"""
    __slots__ = ()

    @classmethod
    def get(cls, **kwargs) -> ProxiesList:
        """
        Parameter (type):
                         Values
                               Description.


        Format (str | .const.Format):
                                     json, txt
                                              Format api output.

        Level (str | list[str] | .const.Level):
                                               transparent, anonymous, elite
                                                                            Anonymity Level.

        Type (str | list[str] | .const.Type):
                                             http, https, socks4, socks5
                                                                        Proxy Protocol.

        Last_Check (int | .const.LastCheck):
                                            Any Number
                                                      Seconds the proxy was last checked.

        Port (int | .const.Port):
                                 Any Number
                                           Proxies with a specific port.

        Ping (int | .const.Ping):
                                 Any Number
                                           How fast you get a response after you've sent out a request.

        Limit (int | .const.Limit):
                                   1 - 20
                                         How many proxies to list.

        Uptime (int | .const.Uptime):
                                     1 - 100
                                            How reliably a proxy has been running.

        Country ((str | list[str]) | .const.Country):
                                                     Example: US, FR
                                                                    Country of the proxy.

        Not_Country (str | list[str] | .const.NotCountry):
                                                          Example: CN, NL
                                                                         Avoid proxy countries.
        """
        ...

    @classmethod
    def raw_request(cls, param: dict[str, str | int]) -> ProxiesList:
        """The same as the get method, only you need to pass a dictionary"""
        ...

    @classmethod
    def already_list(cls, type_: str):
        """Returns a list of ip:port pre-assembled proxies with type type_"""
        ...

    @classmethod
    def eternal_generator(cls, **kwargs) -> Generator[OneProxy | Literal[None], dict[str, str | int]]:
        """
        Returns the eternal proxy generator.
        If no proxy is found according to the specified parameters: yield None
        You can pass a dictionary to send to change the proxy parameters.
        """
        ...

    @classmethod
    def best(cls, **kwargs) -> ProxyDescriptor:
        """Returns the fastest and most reliable proxy, according to the specified parameters."""
        ...
```

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
    Host: str = f'{Ip}:{Port}'

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
        return self.Host

    def __lt__(self, other: ProxyDescriptor) -> bool:
        """Designed for sorting"""
        ...
```

## EasyProxies.const

```python
_TV = typing.TypeVar('_TV')
_TR = typing.TypeVar('_TR')


class Safe(abc.ABC):

    def __new__(cls, values: _TV | typing.Iterable[_TV], raises: bool = False
                ) -> _TR | tuple[_TR]:
        """
        If the raise True argument raises ValueError with an unsuitable value otherwise it returns DEFAULT or None
        """
        ...


class SafeStr(Safe):
    ANY: tuple[str] = ()
    DEFAULT: str = None
    ...


class SafeRange(Safe):
    __slots__ = ()
    MIN: int = 1
    MAX: int
    ...


class SafeCountryCode(Safe): ...


class AnyNumber(int): ...


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


class Port(AnyNumber):
    """Proxies with a specific port"""


class Ping(AnyNumber):
    """How fast you get a response after you've sent out a request"""


class Limit(SafeRange):
    """How many proxies to list."""
    MIN = DEFAULT = 1
    MAX = 20


class Uptime(SafeRange):
    """How reliably a proxy has been running"""
    MIN = 1
    MAX = 100


class Country(SafeCountryCode):
    """Country of the proxy"""


class NotCountry(SafeCountryCode):
    """Avoid proxy countries"""
```
