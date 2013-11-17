import argparse
import sys

def load_args(args):
    parser = argparse.ArgumentParser(prog='connector_2')
    subparsers = parser.add_subparsers()
    parser.add_argument('--version', help='show program version', 
                        action='version', version='1.0')
    
    parser_tcp = subparsers.add_parser('tcp', help='handle tcp connections')
    parser_tcp.add_argument('host', help='host to connect', type=str)
    parser_tcp.add_argument('port', help='port to connect', type=int)
    parser_tcp.add_argument('--timeout', help='connection timeout',
                            type=int, default=30)

    parser_serial = subparsers.add_parser('serial', help='handle serial connections')
    parser_serial.add_argument('port')
    parser_serial.add_argument('--baud', help='baud rate',
                                type=int, default=9600)
    parser_serial.add_argument('--timeout', help='connection timeout',
                               type=int, default=30)

    parsed_args = parser.parse_args()
    print parser.version
    return parsed_args

if __name__ == '__main__':
    print load_args(sys.argv[1:])
