# Script for proxy checking

The script retrieves the proxy list from the txt file, and checks for the proxy's operability and anonymity.

## Using

### proxy_list.txt file example:
```
# you can specify the range of IP addresses
192.168.159.2:9011-192.168.159.4:9011

# you can specify a specific IP address and port
192.168.159.10:9011

# can be specified with or without http: // at the beginning of the line
http://192.168.159.11:9011

127.0.0.1:1111-127.0.0.3:1111
```

### Execution:
if you do not specify a file name on the command line, the script will ask it right after starting
 
```
./check_proxy.py proxy_list.txt
```

### Execution result:
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

* `OK proxies` - the number of proxies that have been checked and are anonymous;
* `Warning proxies` - the number of proxies that transmit the current IP address in the http header, and are not anonymous;
* `Bad proxies` - number of proxies that do not work.

## System requirements
* python 3