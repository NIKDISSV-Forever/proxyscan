from os import remove
from sys import stdout

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from json import load, dump

from time import time
from threading import Thread, ThreadError

class api():

    LEVELS = ("transparent", "anonymous", "elite")
    TYPES = ("http", "https", "socks4", "socks5")
    PORTS = tuple(range(80, 65536))
    UPTIME = tuple(range(1, 101))
    JSON_FILE_NAME = "tmp.result.json"
    STDOUT = bool()
    TIME = 0

    with open("tmp.FILE_HANDLE.txt", 'w') as f:
        FILE_HANDLE = type(f)
    remove("tmp.FILE_HANDLE.txt")

    def __init__(
        self,
        api_link="https://www.proxyscan.io/api/proxy?",
        ret_format=list,
    ):

        """
        
        api_link:
            some URL (str)
                Domain to which the request will be sent
        
        ret_format:
            type list, tuple or type dict or type str
        """

        self.api_link = api_link

        if not ret_format in (list, tuple, dict, str):
            ret_format = list

        self.format = ret_format

        if ((self.format is list or self.format is tuple)
            or (self.format is str or self.format == "txt")):
            self.required_link = self.api_link + "format=txt"
            self._target = True
        elif self.format is dict or self.format == "json":
            self.required_link = self.api_link + "format=json"
            self._target = False
        else:
            self.required_link = self.api_link + "format=txt"
            self._target = True


    def get_url(
        self,

        level=None, lvl=None,

        type_=None, protocol=None,

        last_check=None, l_c=None,

        port=None, pt=None,
        ping=None, pg=None,

        limit=None, max_=None, count=None,

        uptime=None, ut=None,

        country=None, c=None,

        not_country=None, n_c=None, _country=None, _c=None, C=None,

    ):

        """

    level or lvl:
        transparent, anonymous, elite (Const LEVELS)
            Anonymity Level
    
    type_ or protocol:
        http, https, socks4, socks5 (Const TYPES)
            Proxy Protocol
    
    last_check or l_c:
        Any Number (int)
            Seconds the proxy was last checked
    
    port or pt:
        Any Number (Const PORTS)
            Proxies with a specific port

    ping or pg:
        Any Number (int)
            How fast you get a response after you've sent out a request
    
    limit or max_ or count:
        Any Number (int)
            How many proxies to list.

    uptime or ut:
        1 - 100 (Const UPTIME)
            How reliably a proxy has been running
    
    country or c:
        Example: "US,FR" (str or list str or tuple str)
            Country of the proxy
    
    not_country or n_c or _country or _c or C:
        example: ["CN", "NL"] (str or list str or tuple str)
            Avoid proxy countries
        
        """


        if level in self.LEVELS or lvl in self.LEVELS:
            if level in self.LEVELS:
                self.required_link += "&level=" + str(level)
            elif lvl in self.LEVELS:
                self.required_link += "&level=" + str(lvl)

        
        if type_ in self.TYPES or protocol in self.TYPES:
            if type_ in self.TYPES:
                self.required_link += "&type=" + str(type_)
            elif protocol in self.TYPES:
                self.required_link += "&type=" + str(protocol)
        

        if self._is_int(last_check) or self._is_int(l_c):
            if self._is_int(last_check):
                self.required_link += "&last_check=" + str(last_check)
            elif self._is_int(l_c):
                self.required_link += "&last_check=" + str(l_c)
        

        if port in self.PORTS or pt in self.PORTS:
            if port in self.PORTS:
                self.required_link += "&port=" + str(port)
            elif pt in self.PORTS:
                self.required_link += "&port=" + str(pt)
        

        if self._is_int(ping) or self._is_int(pg):
            if self._is_int(ping):
                self.required_link += "&ping=" + str(ping)
            elif self._is_int(pg):
                self.required_link += "&ping=" + str(pg)
        

        if self._is_int(limit) or self._is_int(max_) or self._is_int(count):
            if self._is_int(limit):
                self.end_limit = int(limit)
            elif self._is_int(max_):
                self.end_limit = int(max_)
            elif self._is_int(count):
                self.end_limit = int(count)
        else:
            self.end_limit = 20
        

        if uptime in self.UPTIME or ut in self.UPTIME:
            if uptime in self.UPTIME:
                self.required_link += "&uptime=" + str(uptime)
            elif ut in self.UPTIME:
                self.required_link += "&uptime=" + str(ut)
            

        if country or c:
            if country:
                self._country_test(country, "&country=")
            elif c:
                self._country_test(c, "&country=")
        
        if not_country or n_c or _country or _c or C:
            if not_country:
                self._country_test(not_country, "&not_country=")
            elif n_c:
                self._country_test(n_c, "&not_country=")
            elif _country:
                self._country_test(_country, "&not_country=")
            elif _c:
                self._country_test(_c, "&not_country=")
            elif C:
                self._country_test(C, "&not_country=")
        
        return self.required_link


    def _is_int(self, obj):
        try:
            int(obj)
            return True
        except Exception as Error:
            if self.STDOUT:
                stdout.write(str(Error)+'\n')
            return False


    def _country_test(self, cc, ss):
        if type(cc) is list or type(cc) is tuple:
            self.required_link += ss
            for one in cc:
                self.required_link += str(one) + ','
            self.required_link = self.required_link[:-1]
        elif type(cc) is str:
            self.required_link += ss + cc
    

    def get_proxies(
        self,
        sep='\n',
        out_format=list,
        file=None,
        ):

        """

        sep:
            Any convertible (to str)
                Separator for string format results and writing to file

        out_format:
            Any interable type (list, tuple, str...)
                The type to which the result will be converted

        file:
            File handle (io.TextIOWrapper) or File name (str)
                The file to which the result will be written

        """


        self.required_link += "&limit=" + str(self.end_limit)

        self.result = []


        self.end_with = None

        if self._target:
            target = self._get_proxies_s
        else:
            target = self._get_proxies_d

        while 1:
            
            self.TIME = time()

            try:
                tt = Thread(target=target)
                tt.start()
            except ThreadError as TE:
                if self.STDOUT:
                    stdout.write(str(TE)+'\n')

            if len(self.result) >= self.end_limit:
                self.end_with = True
                end_res = self.result[:self.end_limit]

                if file:
                    if type(file) is self.FILE_HANDLE:

                        if file.mode[0] == 'w' or file.mode[0] == 'a':
                            
                            if self._target:
                                file.write(sep.join(self.result))
                            else:
                                self.save_json(file)

                        else:
                            with open(file.name, 'a', encoding="UTF-8") as file:
                                if self._target:
                                    file.write(sep.join(self.result))
                                else:
                                    self.save_json(file)

                    else:
                        with open(str(file), 'a') as file:
                            file.write(sep.join(self.result))

                self.TIME = time() - self.TIME
                if self._target:

                    if self.format is list or self.format is tuple:
                        return self.format(end_res)
                    else:
                        return sep.join(out_format(end_res))

                else:
                    while 1:
                        try:
                            remove(self.JSON_FILE_NAME)
                            break
                        except Exception as Error:
                            if self.STDOUT:
                                stdout.write(str(Error)+'\n')

                    return out_format(end_res)

            if self.end_with:
                return self.end_with


    def _get_proxies_s(self):
        try:
            resp = urlopen(self.required_link)
            self.result.extend(resp.read().decode("UTF-8").split('\n')[:-1])
        except Exception as Error:
            self.end_with = Error
            if self.STDOUT:
                stdout.write(str(Error)+'\n')
            return
    

    def _get_proxies_d(self):
        try:
            resp = urlopen(self.required_link)
        except Exception as Error:
            self.end_with = Error
            if self.STDOUT:
                stdout.write(str(Error)+'\n')
            return
        utf8resp = resp.read().decode("UTF-8")

        with open(self.JSON_FILE_NAME, 'w') as json_tmp:
            json_tmp.write(utf8resp)
            
        with open(self.JSON_FILE_NAME) as json_data:
            try:
                self.result.extend(load(json_data))
            except Exception as Error:
                if self.STDOUT:
                    stdout.write(str(Error)+'\n')


    def save_json(self, file):
        try:
            dump(self.result, file)
            with open(file.name) as fix:
                fixed = fix.read()

                fixed = fixed.replace('{', "\n\t{\n\t")
                fixed = fixed.replace("},", "\n\t},\n\t")

                fixed = fixed.replace('[', "[\n\t\t")
                fixed = fixed.replace("],", "\n\t\t],\n\t")

                fixed = fixed.replace(", ", ",\n\t")

                with open(file.name, 'w') as r:
                    r.write(fixed)
        except Exception as Error:
            if self.STDOUT:
                stdout.write(str(Error))
            return Error
