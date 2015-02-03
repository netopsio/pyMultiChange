#!/usr/bin/env python

from lib.args import default_args
from lib.args import hosts_file
from lib.args import command_file
from lib.args import protocol
from lib.args import command_output
from lib.args import verbose
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
        access_params = ''
        return """
        You must use a proper connection method.
        Currently telnet and ssh are supported.
        """

    return method, access_params


def log_debug(message):
    import logging
    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)


def log_error(message):
    import logging
    logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    args = default_args(hosts_file, command_file, protocol, command_output,
                        verbose)
    hosts_file = args[0]
    command_file = args[1]
    protocol = args[2].lower()
    command_output = args[3]
    verbose = args[4]

    if not os.path.isfile(hosts_file):
        log_error(message=' Invalid Hosts File')
        exit(1)
    if not os.path.isfile(command_file):
        log_error(message=' Invalid Commands File')
        exit(1)
    access_method = RouterLib()
    hosts = open(hosts_file, 'r')
    log_debug(message=' Reading the hosts file.')
    for host in hosts:
        host = host.strip()
        log_debug(message=' Reading %s from the hosts file.' % host)
        """
        Set up the connection using SSH (default) or Telnet.
        """
        if protocol == 'ssh':
            log_debug(message=' Attempting to access %s via SSH.' % host)
            try:
                log_debug(message=' Establishing ssh connection to %s.' % host)
                access(method='ssh')
                access_cmd = access_params[-1]
                access_shell = access_cmd.invoke_shell()
                shell_output = access_shell.recv(1000)
                if '>' in shell_output:
                    log_debug(message=' Entering enable credentials')
                    access_shell.send('enable\n')
                    time.sleep(1)
                    shell_output = access_shell.recv(1000)
                    if 'Password:' in shell_output:
                        access_shell.send(RouterLib.enable + '\n')
                        time.sleep(1)
                        shell_output = access_shell.recv(1000)
                        if '#' in shell_output:
                            log_debug(message=' Successfully entered enable mode.')
                            access_shell.send('terminal length 0\n')
                            shell_output = access_shell.recv(1000)
                            log_debug(message=' Setting an unlimited terminal buffer.')
                    else:
                        log_debug(message=' Unable to enter enable mode.')
                elif '#' in shell_output:
                    access_shell.send('terminal length 0\n')
                    shell_output = access_shell.recv(1000)
                    log_debug(message=' Setting an unlimited terminal buffer.')
            except:
                log_error(message=' SKIPPING: %s doesn\'t support SSH.' % host)
                exit(1)
        elif protocol == 'telnet':
            log_debug(message=' Attempting to access %s via Telnet.' % host)
            try:
                log_debug(message=' Establishing telnet connection to %s.' % host)
                access(method='telnet')
                access_cmd = access_params[-1]
            except:
                log_error(message=' SKIPPING: %s doesn\'t support Telnet.' % host)
                exit(1)
        else:
            access(method='none')
        """
        Run through the commands in the commands files.
        """
        cmds = open(command_file, 'r')
        log_debug(message=' Reading the commands file.')
        for command in cmds:
            command = command.strip()
            log_debug(message=' Executing: %s' % command)
            if protocol == 'ssh':
                access_shell.send(command + '\n')
                time.sleep(2)
                shell_output = access_shell.recv(1000000)
                if command_output is True:
                    print shell_output
            if protocol == 'telnet':
                access_cmd.write(command + '\n')
                shell_output = access_cmd.read_until('#', 2)
                log_debug(message=' Executing: %s' % command)
                if command_output is True:
                    print shell_output
        """
        Close the sessions and files.
        """
        access_cmd.close()
        log_debug(message=' Closing connection to %s.' % host)
        cmds.close()
        log_debug(message=' Closing commands file.')
    hosts.close()
    log_debug(message=' Closing hosts file.')
