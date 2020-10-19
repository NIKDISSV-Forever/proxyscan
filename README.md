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


# Аргументы:

Функция ```scan``` имеет множество аргументов, для кастомизации прокси.


## level - Уровень анонимности.
Варианты:

```scan(level='transparent' / 'anonymous' / 'elite')```

## type - Протокол прокси.
Варианты:

```scan(type='http' / 'https' / 'socks4' / 'socks5')```

## last_check - Время последней проверки прокси в секундах.
Варианты:

```scan(last_check=Любое число)```

Пример:

```scan(last_check=3600)```

## port - Прокси с определенным портом.
Варианты:

```scan(port=Любое число)```

Пример:

```scan(port=80)```

## uptime - Насколько надежно работает прокси.
Варианты:

```scan(uptime=1-100)```

Пример:

```scan(uptime=50)```

Также, можно указать и больше 100-а, например 400, но вряд-ли вы получите результат.

## country - Страна прокси.
Пример:

```scan(country='US,FR')```

## not_country - Избегать стран прокси.
Пример:

```scan(not_country='CN,NL')```
