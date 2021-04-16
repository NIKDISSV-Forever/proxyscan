# ProxyScanIO

Модуль Python с помощью которого вы можете получить список прокси ip:port, любой длины, бесплатно, с множеством параметров для кастомизации.

Можно создать кортеж Python или сохранить результаты в файл.


# Установка

### Linux

#### Terminal:
> apt install git python3 || pkg install git python3
>
> git clone https://github.com/NIKDISSV-Forever/proxyscan
> 
> cd proxyscan && python3 setup.py install


### Windows

*[Download Python3](https://www.python.org/downloads/)*

*[Download Git](https://git-scm.com/download)*

#### cmd:
> git clone https://github.com/NIKDISSV-Forever/proxyscan
> 
> cd proxyscan && python3 setup.py install

# Использование:

```python3
from proxyscan import ProxyScanIO
proxyScanner = ProxyScanIO()
proxies = proxyScanner.get_proxies()
print(*proxies, sep="\n")
```