#!/usr/bin/env python3

import socket
import urllib.request as req
import urllib.error as req_e
from urllib.parse import urlparse
import re
import os
import sys
import json

# this URL will be used to check proxy.
# for a given link, it is necessary to display information 
# about the connected client in this format (json):
# {"ip":"21.10.121.102"}
PROXY_CHECK_URL = 'https://branchup.pro/whatsmyip.php'

def check_proxy(scheme, ip, port):
	try:
		proxy_addr = '%s://%s:%s' % (scheme, ip, port)
		req.urlcleanup()
		proxy = req.ProxyHandler({'http': proxy_addr, 'https': proxy_addr})
		opener = req.build_opener(proxy)
		req.install_opener(opener)
		conn = req.urlopen(PROXY_CHECK_URL)
		return conn.read()
	except req_e.URLError as e:
		return False

if __name__ == '__main__':
	counts = {
			'error': 0,
			'ok': 0,
			'warn': 0,
		}

	# set default timeout for all connections
	socket.setdefaulttimeout(3)

	class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

	def fix_address(address):
		try:
			if address[:7] != 'http://':
				address = 'http://%s' % address
		except:
			pass

		return address

	def main():
		proxy_list_filename = None

		# check if proxy list file name passed in arguments
		if len(sys.argv) > 1:
			proxy_list_filename = sys.argv[1]

		# check proxy list file exists
		while True:
			if proxy_list_filename is None:
				proxy_list_filename = input('Proxy list file name (Default: proxy_list.txt): ')

			if proxy_list_filename == '':
				proxy_list_filename = 'proxy_list.txt'

			if os.path.isfile('proxy_list.txt') is False:
				print('File not exists!')
				continue

			break

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
					result_text = proxy_check_result.decode('utf8').strip()

					proxy_check_result_txt = ''
					try:
						json_data = json.loads(result_text)

						if 'ip' in json_data:
							if json_data['ip'] == ip:
								proxy_check_result_txt = '%sOK%s' % (bcolors.OKGREEN, bcolors.ENDC)
								counts['ok'] += 1
							else:
								proxy_check_result_txt = '%sFinal IP not equal source%s' % (bcolors.WARNING, bcolors.ENDC)
								counts['warn'] += 1
					except json.decoder.JSONDecodeError:
						proxy_check_result_txt = '%sService cant detect final IP%s' % (bcolors.WARNING, bcolors.ENDC)
						counts['warn'] += 1
					except Exception as e:
						print(type(e))
						proxy_check_result_txt = '%sNot works%s' % (bcolors.FAIL, bcolors.ENDC)
						counts['error'] += 1

					print('%s://%s:%s - %s' % (scheme, ip, port, proxy_check_result_txt))

	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
	finally:
		print('\n\nRESULT:')
		print('OK proxies:', counts['ok'])
		print('Warning proxies:', counts['warn'])
		print('Bad proxies:', counts['error'])
