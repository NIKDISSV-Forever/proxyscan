from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Union, Iterable, Generator

from EasyProxies import const
from EasyProxies._proxy_descriptor import *

__all__ = ('Proxies', 'ProxyDescriptor', 'const')

OneProxy = Union[str, ProxyDescriptor]
ProxiesList = list[OneProxy]


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
        return cls.raw_request(_parse_params(kwargs))

    @classmethod
    def raw_request(cls, param: dict[str, str | int]) -> ProxiesList:
        """The same as the get method, only you need to pass a dictionary"""
        content = _clear_request(f'https://www.proxyscan.io/api/proxy?{urllib.parse.urlencode(param)}')
        try:
            return [ProxyDescriptor(el) for el in json.loads(content)]
        except json.decoder.JSONDecodeError:
            return content.splitlines()

    @classmethod
    def already_list(cls, type_: str):
        """Returns a list of ip:port pre-assembled proxies with type type_"""
        return _clear_request(f'https://www.proxyscan.io/download?type={type_}').splitlines()

    @classmethod
    def eternal_generator(cls, **kwargs) -> Generator[Union[OneProxy, None], dict[str, Union[str, int]]]:
        """
        Returns the eternal proxy generator.
        If no proxy is found according to the specified parameters: yield None
        You can pass a dictionary to send to change the proxy parameters.
        """

        def proxy_generator() -> Generator[Union[OneProxy, None], dict[str, Union[str, int]]]:
            params = _parse_params(kwargs)
            while True:
                proxies = cls.raw_request(params)
                if not proxies:
                    yield
                    continue
                for proxy_desc in proxies:
                    _update_params = yield proxy_desc
                    if _update_params is not None: params = _parse_params(_update_params)

        return proxy_generator()

    @classmethod
    def best(cls, **kwargs) -> ProxyDescriptor:
        """Returns the fastest and most reliable proxy, according to the specified parameters."""
        kwargs = {k.lower(): v for k, v in kwargs.items()}
        if 'limit' not in kwargs: kwargs['limit'] = const.Limit.MAX
        if kwargs.get('format', 'json') != 'json': kwargs['format'] = 'json'
        return sorted(cls.get(**kwargs))[0]


def _parse_params(params: dict[str]) -> dict[str]:
    """Turn a dictionary from **kwargs into a dictionary of parameters for a GET request."""
    _params = {}
    for k, v in params.items():
        if v is None: continue
        if not isinstance(v, str) and isinstance(v, Iterable):
            v = ','.join(i if isinstance(i, str) else str(i) for i in v if i is not None)
        _params[(k if isinstance(k, str) else str(k)).lower()] = v
    return _params


def _clear_request(url: str) -> str: return urllib.request.urlopen(url).read().strip().decode('UTF-8')
