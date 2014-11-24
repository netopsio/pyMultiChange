pyMultiChange
=============

pyMultiChange has two scripts in it. 

* The first is a telnet version - telnet-multi.py
* The second is an ssh version - ssh-multi.py

It utilizes the pyRouterLib. The latest version of pyRouterLib can be obtained at:

https://github.com/jtdub/pyRouterLib

PyMultiChange is a script that allows you to make mass changes to cisco routers and switches.

## telnet-multi.py

The telnet-multi.py script should be fully functional, though I haven't been able to thoroughly test it at scale, yet. To run the script, you pass the -d flag, to specify a hosts file, and the -c flag, to specify the commands file. If you want to enable verbosity of the script, you use the -v True flag, which will enable debugging.

```
usage: telnet-multi.py [-h] [-d HOSTS] -c COMMANDS [-v VERBOSE]

Managing Cisco routers/switches with Python

optional arguments:
  -h, --help            show this help message and exit
  -d HOSTS, --hosts HOSTS
                        Specifies a host file
  -c COMMANDS, --commands COMMANDS
                        Specifies a commands file
  -v VERBOSE, --verbose VERBOSE
                        Be verbose with command output
```

## ssh-multi.py

The ssh-multi.py script isn't fully functional, yet. It will log into many devices and attempt to execute the commands, from a specified commands file, but it will not go into enable mode via the 'enable' command. I'm still working on that functionality. If your routers and switches automatically log you in with enable mode, then you should be good to go, however, if you must specifically use the 'enable' command, then enter your password at the prompt, then the script may not work for you.

```
usage: ssh-multi.py [-h] [-d HOSTS] -c COMMANDS [-v VERBOSE]

Managing Cisco routers/switches with Python

optional arguments:
  -h, --help            show this help message and exit
  -d HOSTS, --hosts HOSTS
                        Specifies a host file
  -c COMMANDS, --commands COMMANDS
                        Specifies a commands file
  -v VERBOSE, --verbose VERBOSE
                        Be verbose with command output
```