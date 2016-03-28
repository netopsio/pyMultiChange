#!/usr/bin/env python

from lib.args import default_args
from netlib.netlib.conn_type import SSH
from netlib.netlib.conn_type import Telnet
from netlib.netlib.user_creds import simple

import logging
import os
import sys
import threading
import Queue


def log_debug(message):
    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)


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
                exit(1)
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
                exit(1)
    else:
        log_debug(message=' Unknown protocol type')
        exit(1)

    access.set_enable(enable_password)
    access.disable_paging()

    with open(commands, 'r') as cmd_file:
        log_debug(message=' Reading the commands file.')
        for command in cmd_file:
            command = command.strip()
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
    creds = simple()

    if not os.path.isfile(args['hosts_file']):
        log_error(message=' Invalid Hosts File.')
        exit(1)
    if not os.path.isfile(args['command_file']):
        log_error(message=' Invalid Commands File.')
        exit(1)

    with open(args['hosts_file'], 'r') as hf:
        hosts = hf.readlines()

    host_settings = list()
    for host in hosts:
        settings = dict()
        settings['device_name'] = host.strip()
        settings['protocol'] = args['protocol']
        settings['username'] = creds['username']
        settings['password'] = creds['password']
        settings['enable_password'] = creds['enable']
        settings['delay'] = args['delay']
        settings['buffer'] = args['buffer']
        settings['commands'] = args['command_file']
        settings['command_output'] = args['command_output']
        host_settings.append(settings)

    if not args['threaded']:
        for host in host_settings:
            device_connection(host)
    else:
        try:
            device_queue = Queue.Queue()
            threads = list()

            for num in range(args['maxthreads']):
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
