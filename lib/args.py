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

    args = vars(parser.parse_args())

    if args['devices']:
        hosts_file = args['devices']
    if args['commands']:
        command_file = args['commands']
    if args['telnet']:
        protocol = 'telnet'
    if args['ssh']:
        protocol = 'ssh'
    if args['output']:
        command_output = args['output']
    if args['verbose']:
        verbose = args['verbose']
    if args['delay']:
        delay = int(args['delay'])
    if args['buffer']:
        buffers = int(args['buffer'])
    if args['threaded']:
        threaded = args['threaded']
    else:
        threaded = False
    if args['maxthreads']:
        maxthreads = int(args['maxthreads'])

    return {'hosts_file': hosts_file, 'command_file': command_file,
            'protocol': protocol, 'command_output': command_output,
            'verbose': verbose, 'delay': delay, 'buffer': buffers,
            'threaded': threaded, 'maxthreads': maxthreads}
