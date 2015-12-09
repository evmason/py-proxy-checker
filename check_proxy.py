#!/usr/bin/env python3

import urllib.request as req
import urllib.error as req_e
from urllib.parse import urlparse
import re
import os

while True:
	proxy_list_filename = input('Proxy list file name (Default: proxy_list.txt): ')

	if proxy_list_filename == '':
		proxy_list_filename = 'proxy_list.txt'

	if os.path.isfile('proxy_list.txt') is False:
		print('File not exists!')
		continue

	break

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def check_proxy(scheme, ip, port):
	try:
		proxy = req.ProxyHandler({scheme: '%s://%s:%s' % (scheme, ip, port)})
		auth = req.HTTPBasicAuthHandler()
		opener = req.build_opener(proxy, auth, req.HTTPHandler)
		req.install_opener(opener)
		conn = req.urlopen('http://stat.corbina.com.ua/')
		return conn.read()
	except req_e.URLError:
		return False

counts = {
	'error': 0,
	'ok': 0,
	'warn': 0,
}

def get_scheme(address):
	scheme = 'http'
	try:
		if address[:8] == 'https://':
			scheme = 'https'
	except:
		pass

	return scheme

def fix_address(address):
	try:
		if address[:7] != 'http://':
			address = 'http://%s' % address
	except:
		pass

	return address

with open(proxy_list_filename) as proxy_list_file:
	for line in proxy_list_file:
		ips_list = []

		line = fix_address(line)

		try:
			line = line.strip()

			if '-' in line:
				ip_start, ip_end = line.split('-')
				port = ''
				o = urlparse(ip_start)
				hostname_start = o.hostname
				if o.scheme is not None:
					scheme = o.scheme

				if o.port is not None:
					port = o.port


				ip_end = fix_address(ip_end)
				o = urlparse(ip_end)
				hostname_end = o.hostname
				if o.scheme is not None:
					scheme = o.scheme

				if o.port is not None:
					port = o.port

				if port is '':
					continue

				ip_parts = hostname_start.split('.')
				ip_base = '%s.%s.%s.' % (ip_parts[0], ip_parts[1], ip_parts[2])
				for i in range(int(hostname_start.split('.')[-1]), int(hostname_end.split('.')[-1]) + 1):
					ips_list.append((scheme, '%s%s' % (ip_base, i), port))
			else:
				o = urlparse(line)

				if o.port is None:
					continue

				port = o.port

				scheme = 'http'
				if o.scheme is not None:
					scheme = o.scheme

				hostname = o.hostname

				ips_list = [(scheme, hostname, port)]
		except:
			continue

		for scheme, ip, port in ips_list:
			proxy_check_result = check_proxy(scheme, ip, port)

			proxy_check_result_txt = '%sNot works%s' % (bcolors.FAIL, bcolors.ENDC)
			if proxy_check_result is not False:
				# Your ip: 31.43.159.120
				search_result = re.search('Your ip: (([0-9]{1,3}\.){3}[0-9]{1,3})', proxy_check_result.decode())
				if search_result:
					final_ip = search_result.group(1)

					if final_ip == ip:
						proxy_check_result_txt = '%sOK%s' % (bcolors.OKGREEN, bcolors.ENDC)
						counts['ok'] += 1
					else:
						proxy_check_result_txt = '%sFinal IP not equal source%s' % (bcolors.WARNING, bcolors.ENDC)
						counts['warn'] += 1
				else:
					proxy_check_result_txt = '%sService cant detect final IP%s' % (bcolors.WARNING, bcolors.ENDC)
					counts['warn'] += 1
			else:
				counts['error'] += 1


			print('%s://%s:%s - %s' % (scheme, ip, port, proxy_check_result_txt))

print('\n\nRESULT:')
print('OK proxies:', counts['ok'])
print('Warning proxies:', counts['warn'])
print('Bad proxies:', counts['error'])