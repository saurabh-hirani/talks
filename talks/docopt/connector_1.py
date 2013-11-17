"""
    connector tcp <host> <port> [--timeout=seconds]
    connector serial <port> [--baud=9600] [--timeout=seconds]
    connector (-h|--help)
"""

import sys
import optparse

def load_args(args):
    parser = optparse.OptionParser()
    parser.add_option('--timeout', help='connection timeout')
    parser.add_option('--baud', help='baud rate')
    options, args = parser.parse_args(args)
    
    if not args:
        raise ValueError()
    
    command = args[0]
    
    if command == 'tcp':
        if len(args) != 3:
            raise ValueError()
        host = args[1]
        port = args[2]
    elif command == 'serial':
        if len(args) != 2:
            raise ValueError()
        host = None
        port = args[1]
    else:
        raise ValueError()
    return (options, command, host, port)
    
if __name__ == '__main__':
    try:
        print load_args(sys.argv[1:])
    except ValueError as e:
        sys.stderr.write('\nERROR: Failed to load args\n')
        sys.stdout.write(__doc__)
        sys.exit(1)
