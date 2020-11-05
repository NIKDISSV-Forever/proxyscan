from os import system as cmd
from threading import Thread
from logging import basicConfig, info, INFO 
from random import choice
from time import time
from math import ceil
#...
try:
	from requests import get
except ModuleNotFoundError:
	print("--- pip install requests ---")
	cmd('pip install requests')
	print("--- pip install requests ---")
	from requests import get

try:
	from fake_useragent import UserAgent
except ModuleNotFoundError:
	print("--- pip install fake-useragent ---")
	cmd("pip install fake-useragent")
	print("--- pip install fake-useragent ---")
	from fake_useragent import UserAgent
#...

global ua
ua = UserAgent()

class proxy:
	
	def scan(
	type='http',
	level=None, 
	port=None, 
	ping=None, 
	last_check=None, 
	uptime=None, 
	country=None, 
	not_country=None, 
	limit=20, 
	timeout=3, 
	proxy=False,
	user_agent=True,
	logs_print=False, 
	logs_file=(False, 'log.log'),
	write_to_file=(False, 'proxy.txt')
				):

		if type:
			type = '&type='+type
		else:
			type = ''
		
		"""
		Types:
		http, https
		socks4, socks5
		"""
		
		if level:
			level = '&level='+level
		else:
			level = ''
		
		"""
		Levels:
		transparent, anonymous, elite
		"""
		
		if port:
			try:
				int(port)
				port = f'&port={port}'
			except:
				port = ''
		else:
			port = ''
		
		if timeout:
			try:
				timeout = float(timeout)
			except:
				timeout = 30
		
		if user_agent:
			headers = {"User-Agent": ua.random}
		else:
			headers = {"User-Agent": None}
		
		if ping:
			try:
				ping = int(ping)
				if ping < 1:
					int('a')
				ping = f'&ping={ping}'
			except:
				ping = ''
		else:
			ping = ''
		if last_check:
			try:
				int(last_check)
				last_check = f'&last_check={last_check}'
			except:
				last_check = '&last_check=3600'
		else:
			last_check = ''
		
		"""
		port, ping, last_check:
		Any Number
		"""
		
		if uptime:
			try:
				uptime = int(uptime)
				if uptime > 999:
					uptime = 100
				uptime = f'&uptime={uptime}'
			except:
				uptime = ''
		else:
			uptime = ''
		
		"""
		uptime:
		1 - 100
		How reliably a proxy has been running.
		"""
		
		if country:
			country = '&country='+country
		else:
			country = ''
		if not_country:
			not_country = '&not_country='+not_country
		else:
			not_country = ''
			
		"""
		country, not_country:
		Example: US, FR
		"""
		if isinstance(write_to_file, list) or isinstance(write_to_file, tuple):
				
			lwtf = len(write_to_file)
			if write_to_file[0]:
				if lwtf >= 2:
					wtfn = str(write_to_file[1])
				else:
					wtfn = 'proxy.txt'
		else:
			if write_to_file:
				wtfn = 'proxy.txt'
		if write_to_file:
			try:
				file = (True, wtfn)
			except:
				file = (True, 'proxy.txt')
		
		"""
		Write to file:
		example: proxy.scan(write_to_file=(True, 'My_proxy_list.txt'))
		"""

		if isinstance(logs_file, list) or isinstance(logs_file, tuple):
				
			llf = len(logs_file)
			if logs_file[0]:
				if llf >= 2:
					lfn = str(logs_file[1])
				else:
					lfn = 'logs_file.log'
		else:
			if logs_file:
				lfn = 'logs_file.log'
		if logs_file:
			try:
				basicConfig(filename=lfn, level=INFO)
			except:
				basicConfig(filename='logs_file.txt', level=INFO)
				
		"""
		Write to debug file:
		example: proxy.scan(logs_file=(True, 'my_debug_file.txt'))
		"""
		
		so_link = f'http://www.proxyscan.io/api/proxy?&format=txt{type}{level}{port}{ping}{last_check}{uptime}{country}{not_country}'		
		if logs_print:
			print(so_link)
			print(headers)
		if logs_file:
			info(so_link)
			info(headers)
		
		def scan_1_list(main_link, lim, proxx):
			while 1:
				try:
					result = get(main_link + f'&limit={lim}', proxies=proxx, timeout=timeout, headers=headers).text.split('\n')
					result = result[0:len(result)-1]
					if result == []:
						main_link = 'http://www.proxyscan.io/api/proxy?&format=txt'
						
						if logs_print:
							print(main_link)
						if logs_file:
							info(main_link)
						
					else:
						break
				except Exception as Error:
					if logs_print:
						print(Error)
					if logs_file:
						info(Error)
			global lister
			lister.extend(result)
			
			if logs_print:
				print(result)
			if logs_file:
				info(result)
			
		global lister
		lister = []
		
		if proxy:
			while 1:
				try:
					prxl = get('http://www.proxyscan.io/api/proxy?&format=txt&type=http&limit=20&uptime=100', timeout=timeout, headers=headers).text.split('\n')
				except Exception as Error:
					if logs_print:
						print(Error)
					if logs_file:
						info(Error)
				if prxl != []:
					break
			prxl = prxl[0:len(prxl) -1]
			limit += 7
		else:
			prxl = [None]
		lims = ceil(limit/20)
			
		if logs_print:
			t1 = time()

		while len(lister) < limit:
			if limit - len(lister) <= 20:
				lim = limit - len(lister)
			else:
				lim = 20
			pp = choice(prxl)
			proxx = {'http': pp}
			if logs_print:
				print(pp)
			if logs_file and pp:
				info(pp)
			
			if lims <= 1:
				scan_1_list(so_link, 20, proxx)
				break
			
			tt = Thread(target=scan_1_list, args=(so_link, lim, proxx,))
			tt.start()
		
		if logs_print:
			print(lister)
			print(len(lister))
			print(len(lister)-limit)
			print(time() - t1)
			
		
		if proxy:
			try:
				rslt = lister[7:limit]
			except IndexError:
				rslt = lister
		
		rslt = lister[0:limit]

		if write_to_file[0]:
			with open (file[1], 'w') as wtfo:
				wtfo.write('\n'.join(rslt))

		return rslt

"""
На самом деле я русский, доксы просто на английском привычнее писать
"""
#NIKDISSV
