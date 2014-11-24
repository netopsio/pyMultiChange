#!/usr/bin/env python

from lib.args import default_args, hosts_file, command_file, verbose
from lib.pyRouterLib import RouterLib
import os

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
			
		#ssh_cmd.exec_command('enable\n' + RouterLib.enable + '\n')
			
		cmds = open(commands_file, 'r')
		
		if verbose is True:
			logging.debug(' Reading commands file.')
				
		for command in cmds:
			command = command.strip()
			
			if verbose is True:
				logging.debug(' Reading %s from the commands file' % command)
				
			stdin, stdout, stderr = ssh_cmd.exec_command(command)
			
			if verbose is True:
				for o in stdout:
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
