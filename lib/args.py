import argparse

hosts_file = ''
command_file = ''
verbose = False


def default_args(hosts_file, command_file, verbose):
    parser = argparse.ArgumentParser(description='Managing Cisco routers/switches with Python')
    parser.add_argument('-d', '--hosts', help='Specifies a host file')
    parser.add_argument('-c', '--commands',  help='Specifies a commands file', required=True)
    parser.add_argument('-v', '--verbose', help='Be verbose with command output')

    args = vars(parser.parse_args())

    if args['hosts']:
        hosts_file = args['hosts']
    if args['commands']:
        command_file = args['commands']
    if args['verbose']:
        args['verbose'] = True
        verbose = args['verbose']

    return hosts_file, command_file, verbose
