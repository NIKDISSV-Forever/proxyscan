from json import loads
from typing import Union, Literal, Iterator
from urllib.parse import urlencode, urljoin, parse_qsl
from urllib.request import urlopen

from EasyProxies import filters

__all__ = ('Proxies', 'filters')

ParamsType = dict[str, Union[str, int]]
ListOfProxy = list[Union[dict[str, Union[str, int, Literal[None]]], str]]
DEFAULT_FILTERS: filters.Filter = filters.FormatTXT


class Proxies:
    __slots__ = ()
    HOST = 'https://www.proxyscan.io/'

    def __init__(self, set_default: Union[filters.Filter, dict] = DEFAULT_FILTERS, set_host: str = HOST):
        global DEFAULT_FILTERS
        if not isinstance(set_default, filters.Filter):
            if not isinstance(set_default, dict):
                set_default = dict(set_default)
            set_default = filters.to_filter(set_default)
        if set_default != DEFAULT_FILTERS:
            DEFAULT_FILTERS = set_default
        if set_host != self.HOST:
            self.__class__.HOST = set_host

    @classmethod
    def _urlopen_read(cls, url: str) -> str:
        return urlopen(url).read().rstrip().decode('UTF-8')

    @classmethod
    def _join_params(cls, params: ParamsType) -> str:
        return urljoin(cls.HOST, f'api/proxy?{urlencode(params)}')

    @classmethod
    def raw_request(cls, params: Union[ParamsType, str]) -> ListOfProxy:
        if not isinstance(params, dict):
            if isinstance(params, filters.Filter):
                params = params.as_dict
            elif isinstance(params, str):
                params = parse_qsl(params)
            else:
                params = dict(params)
        answer = cls._urlopen_read(cls._join_params(params))
        return loads(answer) if params.get('format', 'json').lower() == 'json' else answer.split('\n')

    @classmethod
    def get(cls, filters_: Union[filters.Filter, ParamsType, str] = None, **kw_filters) -> ListOfProxy:
        if filters_ is None:
            filters_ = DEFAULT_FILTERS
        if isinstance(filters_, filters.Filter):
            filters_ = filters_.as_dict
        if kw_filters:
            filters_ |= kw_filters
        return cls.raw_request(DEFAULT_FILTERS.as_dict | filters_)

    @classmethod
    def download_type(cls, protocol: Union[filters.Type, str, int]) -> list[str]:
        if not isinstance(protocol, filters.Type):
            protocol = filters.Type(protocol)
        return cls._urlopen_read(urljoin(cls.HOST, f"download?{protocol}")).split('\n')

    @classmethod
    def generator(cls, *args, perpetual: bool = True, **kwargs) -> Iterator[ListOfProxy]:
        """Proxy generator, if perpetual, it will generate for the given parameters forever"""
        if perpetual:
            def generator() -> Iterator[ListOfProxy]:
                while True:
                    yield from cls.get(*args, **kwargs)
        else:

            def generator() -> Iterator[ListOfProxy]:
                yield from cls.get(*args, **kwargs)

        return generator()
