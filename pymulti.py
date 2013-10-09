#!/usr/bin/env python

import getpass, sys, telnetlib, os, argparse

# Variables
tacacs = '.tacacslogin'
verbose = False 
devicetype = 'ios'
hostsfile = ''
commandsfile = ''

def main():
    # Parse and display argument variables
    global verbose, devicetype, hostsfile, commandsfile
    parser = argparse.ArgumentParser(description='Managing Cisco routers/switches with Python')
    parser.add_argument('-d', '--hosts', help='Specifies a host file')
    parser.add_argument('-c', '--commands',  help='Specifies a commands file', required=True)
    parser.add_argument('-v', '--verbose', help='Be verbose with command output')
    parser.add_argument('-n', '--nexus', help='Execute script assuming Nexus hosts')

    args = vars(parser.parse_args())

    if args['hosts']:
        hostsfile = args['hosts'] 
    if args['commands']:
        commandsfile = args['commands']
    if args['verbose']:
        args['verbose'] = True
        verbose = args['verbose']
    if args['nexus']:
        devicetype = 'nexus'

    return hostsfile, commandsfile, devicetype, verbose

main()

def userlogin():
    # Getting login credentials
    global username, password, enable
    if os.path.isfile(tacacs):
        login = open(tacacs, "r")
        username = login.readline()
        username = username.replace("\n", "")
        password = login.readline()
        password = password.replace("\n", "")
        enable = login.readline()
        enable = enable.replace("\n", "")
        login.close()
    else:
        print tacacs, "not found.\n"
        username = raw_input("Username: ")
        password = getpass.getpass("User Password: ")
        enable = getpass.getpass("Enable Password: ")

    return username, password, enable

def login(devicetype):
    # Logging in with username, password, and eable password
    global username, password, enable
    if devicetype == "nexus":
        telnet.read_until("Login: ")
        telnet.write(str(username) + "\n")
    else:
        telnet.read_until("Username: ")
        telnet.write(str(username) + "\n")

    if password:
        telnet.read_until("Password: ")
        telnet.write(str(password) + "\n")

    if devicetype == "ios":
        if enable:
            telnet.read_until(host2login + '>')
            telnet.write("enable\n")
            telnet.read_until("Password: ")
            telnet.write(str(enable) + "\n")

def sessioncommands():
    # Executing commands on the host
    global commands
    print "Executing Commands on", host2login
    if os.path.isfile(commandsfile):
        commands = open(commandsfile, "r")
        try:
            for cmd2exe in commands:
                telnet.write(cmd2exe)
        finally:
            commands.close()
    else:
        print commandsfile, " doesn't exist"
        telnet.write("exit\n")
    # Displaying the results
    if verbose == True:
        output = telnet.read_all()
        if "% " in output:
            print "Error: ", output
            sys.exit()
        else:
            print output

    print "Logging out of", host2login

# Doing work 
userlogin()
if os.path.isfile(hostsfile):
    hosts = open(hostsfile, "r")
    while 1:
        host2login = hosts.readline()
        host2login = host2login.replace("\n", "")
        print "Logging into", host2login
        if not host2login:
            break
        else:
            telnet = telnetlib.Telnet(host2login)
            login(devicetype)
            sessioncommands()
    hosts.close()
else:
    host2login = raw_input("Host: ")
    print "Logging into", host2login
    telnet = telnetlib.Telnet(host2login)
    login(devicetype)
    sessioncommands()
