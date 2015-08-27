#!/usr/bin/env python

from lib.args import default_args
from netlib.netlib.conn_type import SSH
from netlib.netlib.conn_type import Telnet
from netlib.netlib.user_creds import simple

import logging
import os
import sys


def log_debug(message):
    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)


if __name__ == "__main__":
    args = default_args()
    verbose = args['verbose']
    creds = simple()

    if not os.path.isfile(args['hosts_file']):
        log_error(message=' Invalid Hosts File.')
        exit(1)
    if not os.path.isfile(args['command_file']):
        log_error(message=' Invalid Commands File.')
        exit(1)

    with open(args['hosts_file'], 'r') as hf:
        for host in hf:
            host = host.strip()
            ssh_message = " Attempting to log into %s via SSH." % host
            telnet_message = " Attempting to log into %s via Telnet." % host
            log_debug(message=' Reading %s from the host file.' % host)
            if args['protocol'] == 'ssh':
                try:
                    log_debug(message=ssh_message)
                    access = SSH(host, creds['username'], creds['password'])
                    access.connect()
                except:
                    log_debug(message=' Error connecting via SSH.')
                    try:
                        log_debug(message=telnet_message)
                        access = Telnet(host, creds['username'],
                                        creds['password'])
                        access.connect()
                    except:
                        log_debug(message=' Unable to connect to %s' % host)
                        exit(1)
            elif args['protocol'] == 'telnet':
                try:
                    log_debug(telnet_message)
                    access = Telnet(host, creds['username'], creds['password'])
                    access.connect()
                except:
                    log_debug(message=' Erorr connecting via Telnet.')
                    try:
                        log_debug(message=telnet_message)
                        access = SSH(host, creds['username'],
                                     creds['password'])
                        access.connect()
                    except:
                        log_debug(message=' Unable to connect to %s' % host)
                        exit(1)
            else:
                log_debug(message=' ERROR: Unknown connection type.')
                exit(1)
            access.set_enable(creds['enable'])
            access.disable_paging()

            with open(args['command_file'], 'r') as cf:
                log_debug(message=' Reading the commands file.')
                for command in cf:
                    command = command.strip()
                    log_debug(message=' Executing %s' % command)
                    if args['command_output'] is True:
                        print(access.command(command))
                    else:
                        access.command(command)
            log_debug(message=' Closing connection to %s.' % host)
            access.close()
            log_debug(message=' Closing the commands file.')
            cf.close()
        log_debug(message=' Closing the hosts file.')
        hf.close()
