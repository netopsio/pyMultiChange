#!/usr/bin/env python

from netlib.conn_type import SSH
from netlib.conn_type import Telnet
from netlib import user_creds

import argparse
import logging
import os
import sys
import threading
import Queue


def default_args():
    description = "Managing network devices with python"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--devices', help='Specifies a host file',
                        required=True)
    parser.add_argument('-c', '--commands',  help='Specifies a commands file',
                        required=True)
    parser.add_argument('-s', '--ssh', help='Default: Use the SSH protocol',
                        nargs='?', const='ssh')
    parser.add_argument('-t', '--telnet', help='Use the Telnet protocol',
                        nargs='?', const='telnet')
    parser.add_argument('-o', '--output', help='Verbose command output',
                        nargs='?', const=True)
    parser.add_argument('-v', '--verbose', help='Debug script output',
                        nargs='?', const=True)
    parser.add_argument('--delay',
                        help='Change the default delay exec between commands',
                        default='2')
    parser.add_argument('--buffer',
                        help='Change the default SSH output buffer',
                        default='8192')
    parser.add_argument('--threaded',
                        help='Enable process threading',
                        nargs='?', const=True)
    parser.add_argument('-m', '--maxthreads',
                        help='Define the maximum number of threads',
                        default='10')

    return vars(parser.parse_args())


def log_debug(message):
    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)


def log_failure(device_name, log_file='failure.log'):
    if os.path.isfile(log_file):
        with open(log_file, 'a') as f:
            f.write('{}\n'.format(device_name))
    else:
        with open(log_file, 'w') as f:
            f.write('{}\n'.format(device_name))


def device_connection(device_settings):
    device_name = device_settings['device_name']
    protocol = device_settings['protocol']
    username = device_settings['username']
    password = device_settings['password']
    enable_password = device_settings['enable_password']
    delay = device_settings['delay']
    buffer = device_settings['buffer']
    commands = device_settings['commands']
    command_output = device_settings['command_output']
    ssh_message = " Attempting to log into {} via SSH.".format(device_name)
    telnet_message = " Attempting to log into {} via Telnet.".format(
        device_name)

    ssh_conn = SSH(device_name=device_name,
                   username=username,
                   password=password,
                   delay=delay,
                   buffer=buffer)

    telnet_conn = Telnet(device_name=device_name,
                         username=username,
                         password=password,
                         delay=delay)

    if protocol == 'ssh':
        try:
            log_debug(message=ssh_message)
            access = ssh_conn
            access.connect()
        except:
            log_debug(message=' Error connecting via {}'.format(protocol))
            try:
                log_debug(message=telnet_message)
                access = telnet_conn
                access.connect()
            except:
                log_debug(
                    message=' Unable to connect to {}.'.format(device_name))
                log_failure(device_name)
                pass
    elif protocol == 'telnet':
        try:
            log_debug(message=telnet_message)
            access = telnet_conn
            access.connect()
        except:
            log_debug(message=' Error connecting via {}'.format(protocol))
            try:
                access = ssh_conn
                access.connect()
            except:
                log_debug(
                    message=' Unable to connect to {}.'.format(device_name))
                log_failure(device_name)
                pass
    else:
        log_debug(message=' Unknown protocol type')
        exit(1)

    access.set_enable(enable_password)
    access.disable_paging()

    for command in commands:
        log_debug(message=' Executing {}'.format(command))
        if command_output:
            print(access.command(command))
        else:
            access.command(command)

    log_debug(message=' Closing the connection to {}'.format(device_name))
    access.close()


def connection_queue(queued_device):
    while True:
        try:
            device_settings = device_queue.get(timeout=5)
        except Queue.Empty, ex:
            break
        device_connection(device_settings)
        device_queue.task_done()


if __name__ == "__main__":
    args = default_args()
    verbose = args['verbose']
    creds = user_creds.simple()

    if not os.path.isfile(args['devices']):
        log_error(message=' Invalid Hosts File.')
        exit(1)
    if not os.path.isfile(args['commands']):
        log_error(message=' Invalid Commands File.')
        exit(1)

    if args['telnet']:
        args['protocol'] = 'telnet'
    else:
        args['protocol'] = 'ssh'

    with open(args['devices'], 'r') as hf:
        log_debug(message='Populating hosts')
        hosts = hf.readlines()

    commands = list()

    with open(args['commands'], 'r') as cf:
        log_debug(message='Populating commands')
        for cmd in cf:
            commands.append(cmd.rstrip())

    host_settings = list()
    for host in hosts:
        settings = dict()
        settings['device_name'] = host.strip()
        settings['protocol'] = args['protocol']
        settings['username'] = creds['username']
        settings['password'] = creds['password']
        settings['enable_password'] = creds['enable']
        settings['delay'] = int(args['delay'])
        settings['buffer'] = int(args['buffer'])
        settings['commands'] = commands
        settings['command_output'] = args['output']
        host_settings.append(settings)

    if not args['threaded']:
        for host in host_settings:
            device_connection(host)
    else:
        try:
            device_queue = Queue.Queue()
            threads = list()

            for num in range(int(args['maxthreads'])):
                thread = threading.Thread(
                    target=connection_queue,
                    args=[device_queue])
                thread.start()
                threads.append(thread)

            for host in host_settings:
                device_queue.put(host)

            for t in threads:
                t.join()
        except KeyboardInterrupt:
            exit(1)
