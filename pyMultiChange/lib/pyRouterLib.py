#!/usr/bin/env python

class RouterLib(object):
	
	""" CREDENTIALS Module """
	from os.path import expanduser
	import os.path
	import getpass
	creds_file = expanduser('~/.tacacslogin')
	if os.path.isfile(creds_file):
		f = open(creds_file, 'r')
		username = f.readline().strip()
		password = f.readline().strip()
		enable = f.readline().strip()
		f.close()
	else:
		print "Creating %s" % creds_file
		username = raw_input("Username: ")
		password = getpass.getpass("User Password: ")
		enable = getpass.getpass("Enable Password: ")
		
		f = open(creds_file, 'w')
		f.write(username + "\n" + password + "\n" + enable + "\n")
		f.close()
	
	def __init__(self):
		pass
	
	""" DEBUG Module """
	def enable_debug(self):
		import logging
		logging.basicConfig(level=logging.DEBUG)
		verbose = True
		
		return verbose

	""" TELNET Module """
	"""
	telnetlib documentation:
	https://docs.python.org/2/library/telnetlib.html
	"""
	def use_telnet(self, host, username, password):
		import telnetlib
		import sys
		
		self.host = host
		self.username = username
		self.password = password
		self.access = telnetlib.Telnet(self.host)
		login_prompt = self.access.read_until(": ", 1)
		if 'login' in login_prompt:
			self.is_nexus = True
			self.access.write(username + "\n")
		elif 'Username' in login_prompt:
			self.is_nexus = False
			self.access.write(username + "\n")
		password_prompt = self.access.read_until('Password:', 1)
		self.access.write(password + "\n")
		if self.is_nexus is True:
			self.access.read_until("#")
			self.access.write("terminal length 0\n")
		else:
			self.access.read_until(">")
			self.access.write("enable\n")
			self.access.read_until("Password: ")
			self.access.write(RouterLib.enable + "\n")
			self.access.read_until("#")
			self.access.write("terminal length 0\n")
			self.access.read_until("#")

		return self.host, self.username, self.password, self.is_nexus, self.access
	
	""" SSH Module """
	"""
	Paramiko Documentation:
	http://docs.paramiko.org/en/1.15/api/client.html
	"""
	def use_ssh(self, host, username, password):
		import paramiko
		
		self.host = host
		self.username = username
		self.password = password
		self.access = paramiko.SSHClient()
		self.access.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.access.connect(host, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)
		
		return self.host, self.username, self.password, self.access
	
	""" SNMP Module """	
	def use_snmp(self):
		from os.path import expanduser
		import os.path
		import pysnmp
		community_file = expanduser('~/.community')
		if os.path.isfile(community_file):
			f = open(community_file, 'r')
			self.read_only = f.readline().strip('\n')
			self.read_write = f.readline().strip('\n')
			f.close()
		else:
			print "Creating %s" % community_file
			self.read_only = raw_input("Read-only Community: ")
			self.read_write = raw_input("Read-write Community: ")
			
			f = open(community_file, 'w')
			f.write(self.read_only + "\n" + self.read_write + "\n")
			f.close()
		
		return self.read_only, self.read_write


