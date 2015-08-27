import argparse

protocol = 'ssh'
command_output = False
verbose = False


def default_args():
    global protocol, command_output, verbose
    description = "Managing network devices with python"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--hosts', help='Specifies a host file',
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

    args = vars(parser.parse_args())

    if args['hosts']:
        hosts_file = args['hosts']
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

    return {'hosts_file': hosts_file, 'command_file': command_file,
            'protocol': protocol, 'command_output': command_output,
            'verbose': verbose}
