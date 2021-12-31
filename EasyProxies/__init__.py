from json import loads
from typing import Union
from urllib.parse import parse_qsl, urlencode, urljoin
from urllib.request import urlopen

from EasyProxies import filters

__all__ = ('Proxies', 'filters')

ParamsType = dict[str, Union[str, int]]
ListOfProxy = list[Union[dict[str, Union[str, int, type(None)]], str]]

DEFAULT_FILTERS = filters.FormatTXT


class Proxies:
    __slots__ = ()
    HOST = 'https://www.proxyscan.io/'

    def __init__(self, default: filters.Filter, host: str = HOST):
        global DEFAULT_FILTERS
        DEFAULT_FILTERS = default
        self.__class__.HOST = host

    @classmethod
    def _urlopen_read(cls, url: str) -> str:
        return urlopen(url).read().rstrip().decode('UTF-8')

    @classmethod
    def _join_params(cls, params: ParamsType) -> str:
        return urljoin(cls.HOST, f'api/proxy?{urlencode(params)}')

    @classmethod
    def raw_request(cls, params: Union[ParamsType, str]) -> ListOfProxy:
        params = dict(parse_qsl(str(params))) if isinstance(params, (str, filters.Filter)) else {
            i.lower(): k.lower() if isinstance(k, str) else k for i, k in params.items()
        }
        answer = cls._urlopen_read(cls._join_params(params))
        return loads(answer) if params.get('format', 'json').lower() == 'json' else answer.split('\n')

    @classmethod
    def get(cls, filters: Union[filters.Filter, ParamsType, str] = DEFAULT_FILTERS) -> ListOfProxy:
        return cls.raw_request(filters)

    @classmethod
    def download_type(cls, protocol: filters.Type) -> list[str]:
        return cls._urlopen_read(urljoin(cls.HOST, f"download?{urlencode({'type': protocol.value})}")).split('\n')
