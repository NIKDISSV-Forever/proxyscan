from __future__ import annotations

from functools import total_ordering
from typing import Union, ForwardRef

__all__ = ('JsonProxy', 'ProxyDescriptor')

from EasyProxies import const

JsonProxy = dict[str, Union[str, int, type(None)]]


class _AnyDescriptor:
    def __init__(self, from_json: dict[str]):
        values = {}
        for k, v in from_json.items():
            if isinstance(v, dict):
                class _value(_AnyDescriptor, name=k):
                    pass

                v = _value(v)
            values[k] = v
        self.__dict__ = values
        self.as_dict = from_json

    def __init_subclass__(cls, **kwargs):
        if 'name' in kwargs: cls.__name__ = kwargs['name']

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


@total_ordering
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
        TYPE = {i.lower() for i in self.Type}
        for sock_type in sorted({i.lower() for i in const.Type.SOCKS}, key=lambda i: int(i[-1]), reverse=True):
            for my_type in TYPE:
                if my_type == sock_type:
                    ip = f'{my_type}://{self}'
                    return {'http': ip, 'https': ip}
        return {protocol: f'{protocol}://{self}' for protocol in TYPE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Host = f'{self.Ip}:{self.Port}'

    def __str__(self):
        """Like format='txt'"""
        return self.Host

    def __lt__(self, other: ForwardRef('ProxyDescriptor')) -> bool:
        """Designed for sorting"""
        if self.Failed != other.Failed:
            return self.Failed
        elif self.Ping < other.Ping:
            return True
        elif self.Ping == other.Ping:
            if self.Uptime > other.Uptime:
                return True
            elif self.Uptime == other.Uptime:
                self_anon = const.Level.ANY.index(self.Anonymity.lower())
                other_anon = const.Level.ANY.index(other.Anonymity.lower())
                if self_anon < other_anon:
                    return True
                elif self_anon == other_anon:
                    return self.Time >= other.Time
        return False
