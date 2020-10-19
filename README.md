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

```from proxyscan import proxy```

```proxy_list = proxy.scan()```


# Аргументы:

Функция ```scan()``` имеет множество аргументов, для кастомизации прокси.

## limit - Количество адресов прокси ```int```.
Варианты:

```scan(limit=Любое число)```

Пример:

```scan(limit=100)```

По умолчанию: 

```limit=20```, а именно, один запрос с лимитом 20, т.е не больше 20-и.

## level - Уровень анонимности ```str```.
Варианты:

```scan(level='transparent' / 'anonymous' / 'elite')```

## type - Протокол прокси ```str```.
Варианты:

```scan(type='http' / 'https' / 'socks4' / 'socks5')```

По умолчанию:

```type='http'```

## last_check - Время последней проверки прокси в секундах ```int```.
Варианты:

```scan(last_check=Любое число)```

Пример:

```scan(last_check=3600)```

## port - Прокси с определенным портом ```int```.
Варианты:

```scan(port=Любое число)```

Пример:

```scan(port=80)```

## uptime - Насколько надежно работает прокси ```int```.
Варианты:

```scan(uptime=1-100)```

Пример:

```scan(uptime=50)```

Также, можно указать и больше 100-а, например 400, но вряд-ли вы получите результат.

## country - Страна прокси ```str```.
Пример:

```scan(country='US,FR')```

## not_country - Избегать стран прокси ```str```.
Пример:

```scan(not_country='CN,NL')```


## proxy - использовать прокси при отправке запроса ```bool```.
Принимает bool значение т.е:

```scan(proxy=1 / True)``` - Прокси будет использоваться.

```scan(proxy=0 / False)``` - Прокси использоваться не будет.

По умолчанию:

```proxy=False```

Поскольку у api количество запросов не ограничено…

Использование прокси при запросе, вовсе не обязательно, и только замедлит скорость работы.

## logs_print - Отображать ли действия скрипта, в консоли ```bool```.
Принимает bool значение т.е:

```scan(logs_print=1 / True)``` - Отображать.

```scan(logs_print=0 / False)``` - Не отображать.

По умолчанию:

```logs_print=False```

## logs_file - Логировать ли действия скрипта в файле ```tuple``` / ```list``` / ```bool```.
Принимает список/кортеж состоящий из 2-х элементов.

Первый элемент - значение bool, т.е

```1 / True``` - записывать.
```0 / False``` - не записывать.

Второй элемент - ```str``` название файла.

Пример:

```scan(logs_file=(1, 'file.log'))```

Если не указывать имя файла.

По умолчанию имя файла 'logs_file.log', т.е

Пример:

```scan(logs_file=1)```
