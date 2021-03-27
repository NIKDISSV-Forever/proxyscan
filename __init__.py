from threading import Thread
from json import loads

from typing import Tuple, Union
from http.client import HTTPResponse

from urllib.request import urlopen


class GetProxiesError(Exception):
	pass


class ProxyScanIO:

	API_URL = "https://www.proxyscan.io/api/proxy?"

	@staticmethod
	def is_digit(obj=None) -> bool:
		return isinstance(obj, int) or isinstance(obj, float)
	
	def __init__(self, API_URL: str = API_URL,
	             error_with_empty: int = 3,
	             suppressing_exceptions: bool = True,
	             print_to=False) -> None:
		
		self.error_with_empty = error_with_empty
		self.suppressing_exceptions = suppressing_exceptions
		self.print_to = print_to
		if API_URL != self.API_URL:
			self.API_URL = API_URL
	
	def get_proxies(self,
	                count: int = None,
	                **kwargs
	                ) -> Tuple[Union[str, dict]]:
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
		
		if self.is_digit(count):
			self._limit = (count if isinstance(count, int)
			               else int(count))
		else:
			self._limit = None
		self._end_link = self.API_URL
		
		self.use_json = False
		if "format" in kwargs:
			self.use_json = kwargs["format"].lower() == "json"
		else:
			kwargs["format"] = "txt"
		for param in kwargs:
			value = kwargs[param]
			self._end_link += f"{param.lower()}={value}&"
		
		self.__make_requests()
		if self.print_to is not False:
			print("\n".join(self._result), file=self.print_to)
		return self._result
	
	def __add_result(self, limit: Tuple[int] = (20, 20)) -> None:
		proxies = tuple()
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
		
		self._result = tuple()
		threads = tuple()
		
		if self._limit:
			integer: tuple = (1,) * (self._limit // 20)
			non_int = self._limit % 20 / 20,
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
	help(ProxyScanIO)
