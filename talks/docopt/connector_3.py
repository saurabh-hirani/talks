"""
Usage:
    connector tcp <host> <port> [--timeout=<seconds>]
    connector serial <port> [--baud=<baud_rate>] [--timeout=<seconds>]
    connector (-h|--help|--version)

Options:
    -h|--help             show this help text
    --version             print this version
    --timeout=<seconds>   connection timeout [default: 30]
    --baud=<baud_rate>    baud rate of modem [default: 9600]

"""
from docopt import docopt
import sys

def load_args(args):
    parsed_docopt = docopt(__doc__, version='1.0')
    return parsed_docopt

if __name__ == '__main__':
    print load_args(sys.argv[1:])
