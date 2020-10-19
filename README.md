# proxyscan
Модуль Python с помощью которого вы можете получить список прокси ip:port, любой длины, бесплатно, с множеством параметров для кастомизации.
Можно создать список Python или сохранить результаты в файл.

# Установка


pkg/apt install git


git clone https://github.com/NIKDISSV-Forever/proxyscan.git; cd proxyscan; python setup.py install; cd ..; rm -rf proxyscan

Или:

git clone https://github.com/NIKDISSV-Forever/proxyscan.git

Или:

pip install --index-url https://test.pypi.org/simple --no-deps proxyscan-io-api

# Использование:

```from proxyscan import proxyscan```

```proxy = proxyscan.proxy```

```proxy_list = proxy.scan()```
