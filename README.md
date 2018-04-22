# Скрипт для проверки прокси

[![Latest Stable Version](https://poser.pugx.org/evmason/py-proxy-checker/v/stable)](https://packagist.org/packages/evmason/py-proxy-checker)
[![Total Downloads](https://poser.pugx.org/evmason/py-proxy-checker/downloads)](https://packagist.org/packages/evmason/py-proxy-checker)
[![Latest Unstable Version](https://poser.pugx.org/evmason/py-proxy-checker/v/unstable)](https://packagist.org/packages/evmason/py-proxy-checker)
[![License](https://poser.pugx.org/evmason/py-proxy-checker/license)](https://packagist.org/packages/evmason/py-proxy-checker)

Скрипт получает список прокси из txt файл, и производит проверку на работоспособность и анонимность прокси.

## Использование

### Пример файла proxy_list.txt:
```
# можно указывать диапазон IP адресов
192.168.159.2:9011-192.168.159.4:9011

# можно указывать конкретный IP адрес и порт
192.168.159.10:9011

# можно указывать с или без http:// в начале строки
http://192.168.159.11:9011

127.0.0.1:1111-127.0.0.3:1111
```

### Выполнение:
если не указывать имя файла в командной строке, скрипт спросит его сразу после запуска
 
```
./check_proxy.py proxy_list.txt
```

### Результат выполнения:
```
http://192.168.159.2:9011 - OK
http://192.168.159.3:9011 - OK
http://192.168.159.4:9011 - OK
http://192.168.159.10:9011 - OK
http://192.168.159.11:9011 - OK
http://127.0.0.1:1111 - Not works
http://127.0.0.2:1111 - Not works
http://127.0.0.3:1111 - Not works

RESULT:
OK proxies: 5
Warning proxies: 0
Bad proxies: 3
```

* `OK proxies` - кол. прокси которые прошли проверку и являются анонимными;
* `Warning proxies` - кол. прокси которые передают в http заголовке настоящий IP адрес, и не являются анонимными;
* `Bad proxies` - кол. рокси которые не отвечают.

## Системные требования
* python 3