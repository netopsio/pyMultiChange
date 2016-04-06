pyMultiChange
=============

It utilizes a python library called 'netlib' The latest version of 'netlib' can be obtained at:

https://github.com/jtdub/netlib

## Install

```
git clone git@github.com:jtdub/pyMultiChange.git
cd pyMultiChange
sudo python setup.py install
```

PyMultiChange is a script that allows you to make mass changes to cisco routers and switches.

## multi_change.py

```
usage: multi_change.py [-h] -d DEVICES -c COMMANDS [-s [SSH]] [-t [TELNET]]
                       [-o [OUTPUT]] [-v [VERBOSE]] [--delay DELAY] [--buffer BUFFER]
                       [--threaded [THREADED]] [-m MAXTHREADS]

Managing network devices with python

optional arguments:
  -h, --help            show this help message and exit
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
