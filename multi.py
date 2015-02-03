#!/usr/bin/env python

from lib.new_args import default_args
from lib.new_args import hosts_file
from lib.new_args import command_file
from lib.new_args import protocol
from lib.new_args import command_output
from lib.new_args import verbose
from lib.pyRouterLib import RouterLib

import os
import time
import sys

access_params = ''


def access(method):
    global access_params
    if method == 'ssh':
        access_params = access_method.use_ssh(host, RouterLib.username,
                                              RouterLib.password)
    elif method == 'telnet':
        access_params = access_method.use_telnet(host, RouterLib.username,
                                                 RouterLib.password)
    else:
        access_paams = ''
        return """
        You must use a proper connection method.
        Currently telnet and ssh are supported.
        """

    return method, access_params


if __name__ == '__main__':
    args = default_args(hosts_file, command_file, protocol, command_output,
                        verbose)
    hosts_file = args[0]
    command_file = args[1]
    protocol = args[2].lower()
    command_output = args[3]
    verbose = args[4]

    if not os.path.isfile(hosts_file):
        print "Error: Invalid Hosts File"
        exit(1)
    if not os.path.isfile(command_file):
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
            logging.debug(' Reading %s from the hosts file.' % host)
        """
        Set up the connection using SSH (default) or Telnet.
        """
        if protocol == 'ssh':
            if verbose is True:
                logging.debug(' Attempting to access %s via SSH.' % host)
            try:
                if verbose is True:
                    logging.debug(' Establishing ssh connection to %s.' % host)
                access(method='ssh')
                access_cmd = access_params[-1]
                access_shell = access_cmd.invoke_shell()
                shell_output = access_shell.recv(1000)
                if '>' in shell_output:
                    if verbose is True:
                        logging.debug(' Entering enable credentials')
                    access_shell.send('enable\n')
                    time.sleep(1)
                    shell_output = access_shell.recv(1000)
                    if 'Password:' in shell_output:
                        access_shell.send(RouterLib.enable + '\n')
                        time.sleep(1)
                        shell_output = access_shell.recv(1000)
                        if '#' in shell_output:
                            if verbose is True:
                                logging.debug(' Successfully entered enable mode.')
                            access_shell.send('terminal length 0\n')
                            shell_output = access_shell.recv(1000)
                            if verbose is True:
                                logging.debug(' Setting an unlimited terminal buffer.')
                    else:
                        if verbose is True:
                            logging.debug(' Unable to enter enable mode.')
                elif '#' in shell_output:
                    access_shell.send('terminal length 0\n')
                    shell_output = access_shell.recv(1000)
                    if verbose is True:
                        logging.debug(' Setting an unlimited terminal buffer.')
            except:
                logging.debug(' SKIPPING: %s doesn\'t support SSH.' % host)
                exit(1)
        elif protocol == 'telnet':
            if verbose is True:
                logging.debug(' Attempting to access %s via Telnet.' % host)
            try:
                if verbose is True:
                    logging.debug(' Establishing telnet connection to %s.' % host)
                access(method='telnet')
                access_cmd = access_params[-1]
            except:
                logging.debug(' SKIPPING: %s doesn\'t support Telnet.' % host)
                exit(1)
        else:
            access(method='none')
        """
        Run through the commands in the commands files.
        """
        cmds = open(command_file, 'r')
        if verbose is True:
            logging.debug(' Reading the commands file.')
        for command in cmds:
            command = command.strip()
            if verbose is True:
                logging.debug(' Executing: %s' % command)
            if protocol == 'ssh':
                access_shell.send(command + '\n')
                time.sleep(2)
                shell_output = access_shell.recv(1000000)
                if command_output is True:
                    print shell_output
            if protocol == 'telnet':
                access_cmd.write(command + '\n')
                shell_output = access_cmd.read_until('#', 2)
                if verbose is True:
                    logging.debug(' Executing: %s' % command)
                if command_output is True:
                    print shell_output
        """
        Close the sessions and files.
        """
        access_cmd.close()
        if verbose is True:
            logging.debug(' Closing connection to %s.' % host)
        cmds.close()
        if verbose is True:
            logging.debug(' Closing commands file.')
    hosts.close()
    if verbose is True:
        logging.debug(' Closing hosts file.')
