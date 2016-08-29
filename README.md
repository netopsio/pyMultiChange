pyMultiChange
=============

[![Build Status](https://travis-ci.org/netopsio/pyMultiChange.svg)](https://travis-ci.org/netopsio/pyMultiChange)

It utilizes a python library called 'netlib' The latest version of 'netlib' can be obtained at:

https://github.com/netopsio/netlib

## Install

Netlib requires a couple packages be installed, as a requirement of its SNMP functionality.

### Redhat based Linux distributions

```
sudo yum install net-snmp-devel gcc python-devel
```

### Debian based Linux distributions

```
sudo apt-get install libsnmp-dev snmp-mibs-downloader gcc python-dev
```

```
git clone git@github.com:jtdub/pyMultiChange.git
cd pyMultiChange
sudo python setup.py install
```

PyMultiChange is a script that allows you to make mass changes to cisco routers and switches.

## multi_change.py

```
jtdub-macbook:bin jtdub$ ./multi_change.py --help
usage: multi_change.py [-h] -u USERNAME [--delete-creds [DELETE_CREDS]]
                       [--set-creds [SET_CREDS]] [-d DEVICES] [-c COMMANDS]
                       [-s [SSH]] [-t [TELNET]] [-o [OUTPUT]] [-v [VERBOSE]]
                       [--delay DELAY] [--buffer BUFFER]
                       [--threaded [THREADED]] [-m MAXTHREADS]

Managing network devices with python

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Specify your username.
  --delete-creds [DELETE_CREDS]
                        Delete credentials from keyring.
  --set-creds [SET_CREDS]
                        set keyring credentials.
  -d DEVICES, --devices DEVICES
                        Specifies a host file
  -c COMMANDS, --commands COMMANDS
                        Specifies a commands file
  -s [SSH], --ssh [SSH]
                        Default: Use the SSH protocol
  -t [TELNET], --telnet [TELNET]
                        Use the Telnet protocol
  -o [OUTPUT], --output [OUTPUT]
                        Verbose command output
  -v [VERBOSE], --verbose [VERBOSE]
                        Debug script output
  --delay DELAY         Change the default delay exec between commands
  --buffer BUFFER       Change the default SSH output buffer
  --threaded [THREADED]
                        Enable process threading
  -m MAXTHREADS, --maxthreads MAXTHREADS
                        Define the maximum number of threads
```
