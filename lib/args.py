import argparse

protocol = 'ssh'
command_output = False
verbose = False


def default_args():
    global protocol, command_output, verbose
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
