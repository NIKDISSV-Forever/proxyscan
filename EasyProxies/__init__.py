from json import loads
from typing import Union, Literal, Iterator
from urllib.parse import urljoin, parse_qsl
from urllib.request import urlopen

from EasyProxies import filters

__all__ = ('Proxies', 'filters')

ParamsType = Union[str, filters.Parameters, dict[str]]
ListOfProxy = list[Union[dict[str, Union[str, int, Literal[None]]], str]]
DEFAULT_FILTERS: filters.Parameters = filters.FormatTXT


class Proxies:
    __slots__ = ()
    HOST = 'https://www.proxyscan.io/'

    def __init__(self, set_default: Union[filters.Parameters, dict] = DEFAULT_FILTERS, set_host: str = HOST):
        global DEFAULT_FILTERS
        if not isinstance(set_default, filters.Parameters):
            if not isinstance(set_default, dict):
                set_default = dict(set_default)
            set_default = filters.Parameters(set_default)
        if set_default != DEFAULT_FILTERS:
            DEFAULT_FILTERS = set_default
        if set_host != self.HOST:
            self.__class__.HOST = set_host

    @classmethod
    def _urlopen_read(cls, url: str) -> str:
        return urlopen(url).read().rstrip().decode('UTF-8')

    @classmethod
    def raw_request(cls, params: filters.Parameters) -> ListOfProxy:
        answer = cls._urlopen_read(urljoin(cls.HOST, f'api/proxy?{params}'))
        return loads(answer) if tuple(params.parameters.get('format', ('json',)))[
                                    0].lower() == 'json' else answer.splitlines()

    @classmethod
    def get(cls, filters_: ParamsType = None, **kw_filters) -> ListOfProxy:
        if filters_ is None:
            filters_ = DEFAULT_FILTERS
        elif not isinstance(filters_, filters.Parameters):
            if isinstance(filters_, dict):
                filters_ = filters.Parameters(filters_)
            elif isinstance(filters_, (bytes, str)):
                filters_ = filters.Parameters(dict(parse_qsl(filters_)))
        if kw_filters:
            filters_ = filters.Parameters(filters.marge(filters_.parameters, kw_filters))
        return cls.raw_request(filters.Parameters(filters.marge(DEFAULT_FILTERS.parameters, filters_.parameters)))

    @classmethod
    def download_type(cls, protocol: Union[filters.Type, str, int]) -> list[str]:
        if not isinstance(protocol, filters.Type):
            protocol = filters.Type(protocol)
        return cls._urlopen_read(urljoin(cls.HOST, f'download?{protocol}')).split('\n')

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
