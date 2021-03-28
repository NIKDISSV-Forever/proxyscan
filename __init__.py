from typing import IO, Text, Tuple, Union, SupportsInt

from http.client import HTTPResponse
from urllib.request import urlopen

from json import loads, dumps
from threading import Thread


Numeric = Union[SupportsInt, int, float, str, None]
PrintFile = Union[None, bool, IO]
IntendType = Union[None, int, str]
ResultTuple = Tuple[Union[str, dict]]


class GetProxiesError(Exception):
    pass


class ProxyScanIO:

    API_URL: Text = "https://www.proxyscan.io/api/proxy?"

    def __init__(self, API_URL: Text = API_URL,
                 error_with_empty: Numeric = 3,
                 suppressing_exceptions: bool = True,
                 indent: IntendType = 4,
                 print_to: PrintFile = False) -> None:

        self.error_with_empty = int(error_with_empty)
        self.suppressing_exceptions = bool(suppressing_exceptions)
        self.indent = int(indent)
        self.print_to = print_to
        if API_URL != self.API_URL:
            self.API_URL = API_URL

    def get_proxies(self,
                    count: Numeric = None,
                    **kwargs
                    ) -> ResultTuple:

        """
Parameter
            Value
                            Description

Format
            txt, json
                            Format api output

Level
            transparent,
            anonymous,
            elite
                            Anonymity Level

Type
            http, https,
            socks4, socks5
                            Proxy Protocol

Last_Check
            Any Number
                            Seconds the proxy was last checked
Port
            Any Number
                            Proxies with a specific port
Ping
            Any Number
                            How fast you get a response after
                                you've sent out a request
Limit
            1 - 20
                            How many proxies to list.
Uptime
            1 - 100
                            How reliably a proxy has been running
Country
            2 Any Letters
                            Country of the proxy
Not_Country
            2 Any Letters
                            Avoid proxy countries
        """

        if isinstance(count, (int, float)):
            self._limit = int(count)
        else:
            self._limit = None
        self._end_link = self.API_URL

        self.use_json = False
        if "format" in kwargs:
            self.use_json = kwargs["format"].lower() == "json"
        else:
            kwargs["format"] = "txt"

        for param in kwargs:
            self._end_link += f"{param.lower()}={kwargs[param]}&"

        self.__make_requests()

        self.result = self._result[:self._limit]

        if self.print_to is not False:
            if self.use_json:
                p_result = "["
                dumped = (dumps(obj, indent=self.indent) for obj in self.result)
                p_result += ", ".join(dumped)
                p_result += "]"
            else:
                p_result = "\n".join(self.result)

            print(p_result, file=self.print_to)

        return self.result

    def __add_result(self, limit: Tuple[int] = (20, 20)) -> None:

        proxies = ()
        with_empty = self.error_with_empty
        
        while len(proxies) < limit[0]:
            try:
                url = f"{self._end_link}limit={limit[1]}"
                resp: HTTPResponse = urlopen(url)
                page_text = resp.read().decode("UTF-8")
                
                if self.use_json:
                    proxies += tuple(loads(page_text))
                else:
                    proxies += tuple(page_text.splitlines())
                
                if len(proxies) == 0:
                    with_empty -= 1
                self._result += proxies
            except Exception as Error:
                if not self.suppressing_exceptions:
                    raise Error
            if not with_empty:
                raise GetProxiesError("Too many requests were unsuccessful.")
    
    def __make_requests(self) -> None:
        
        self._result = threads = ()
        
        if self._limit:
            integer: Tuple[int] = (1,) * (self._limit // 20)
            non_int: Tuple[float] = self._limit % 20 / 20,
            limit_each = integer + non_int
        else:
            limit_each = None,
        
        for i in limit_each:
            args = ((int(i * 20.),) * 2,) if i else ((1, 20),)
            t = Thread(target=self.__add_result, args=args)
            t.start()
            threads += t,
        for t in threads:
            t.join()


if __name__ == "__main__":
    help(ProxyScanIO())
