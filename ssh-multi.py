#!/usr/bin/env python

from lib.args import default_args, hosts_file, command_file, verbose
from lib.pyRouterLib import RouterLib
import os
import time

if __name__ == '__main__':
	
	""" Pull the default arguments """
	args = default_args(hosts_file, command_file, verbose)
	
	hosts_file = args[0]
	commands_file = args[1]
	verbose = args[2]
	
	if not os.path.isfile(hosts_file):
		print "Error: Invalid Hosts File"
		exit(1)
	if not os.path.isfile(commands_file):
		print "Error: Invalid Commands File"
		exit(1)
		
	if verbose is True:
		import logging
		logging.basicConfig(level=logging.DEBUG)
		
	access_method = RouterLib()
	
	hosts = open(hosts_file, 'r')
	
	if verbose is True:
		logging.debug(' Reading hosts file.')
	
	for host in hosts:
		host = host.strip()
		
		if verbose is True:
			logging.debug(' Reading %s from hosts file.' % host)
			
		ssh = access_method.use_ssh(host, RouterLib.username, RouterLib.password)
		ssh_cmd = ssh[-1]
		
		if verbose is True:
			logging.debug(' Establishing ssh connection to %s.' % host)
			
		ssh_shell = ssh_cmd.invoke_shell()
		o = ssh_shell.recv(1000)
		
		if '>' in o:
			if verbose is True:
				logging.debug(' Attempting to enter enable mode.')
				
			ssh_shell.send("enable\n")
			time.sleep(1)
		
			o = ssh_shell.recv(1000)
			
			if 'Password:' in o:
				
				if verbose is True:
					logging.debug(' Entering enable credentials.')
				
				ssh_shell.send(RouterLib.enable + "\n")
				time.sleep(1)
			
				o = ssh_shell.recv(1000)
				
				if '#' in o:
					if verbose is True:
						logging.debug(' Successfully entered enable mode.')
						
					ssh_shell.send("terminal length 0\n")
					
					o = ssh_shell.recv(1000)
					
					if verbose is True:
						logging.debug(' Setting an unlimited terminal buffer.')
						
			else:
				if verbose is True:
					logging.debug(' Unable to enter enable mode.')
		
		elif '#' in o:
			if verbose is True:
				logging.debug(' Skipping attempt at enable mode as we already have administrative privileges.')
				
			ssh_shell.send("terminal length 0\n")
			
			o = ssh_shell.recv(1000)
			
			if verbose is True:
				logging.debug(' Setting an unlimited terminal buffer.')
		
		else:
			if verbose is True:
				logging.debug(' Something unexpected happened.')
			
		cmds = open(commands_file, 'r')
		
		if verbose is True:
			logging.debug(' Reading commands file.')
				
		for command in cmds:
			command = command.strip()
			
			if verbose is True:
				logging.debug(' Reading %s from the commands file' % command)
				
			ssh_shell.send(command + "\n")
			time.sleep(1)
			
			o = ssh_shell.recv(1000000)
			
			if verbose is True:
				print o
			
			if verbose is True:
				logging.debug(' Executing %s' % command)
			
		if verbose is True:
			logging.debug(' Logging out of %s.' % host)
			
		ssh_cmd.close()
			
		if verbose is True:
			logging.debug(' Closing commands file.')
			
		cmds.close()

	if verbose is True:
		logging.debug(' Closing hosts file.')

	hosts.close()
