# proxyscan
Модуль Python с помощью которого вы можете получить список прокси ip:port, любой длины, бесплатно, с множеством параметров для кастомизации.
Можно создать список Python или сохранить результаты в файл.

# Установка

pkg/apt install git

git clone https://github.com/NIKDISSV-Forever/proxyscan.git; cd proxyscan; python setup.py install; cd ..; rm -rf proxyscan

Или:


git clone https://github.com/NIKDISSV-Forever/proxyscan/ ../usr/lib/python3.8/site-packages/proxyscan __Директория python__


mv ../usr/lib/python3.8/site-packages/proxyscan/proxyscan.py ..; rm -rf ../usr/lib/python3.8/site-packages/proxyscan/


Или:

pip install --index-url https://test.pypi.org/simple --no-deps proxyscan-io-api

# Использование:

```import proxyscan```
```help(proxyscan.api())```
