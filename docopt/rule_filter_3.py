"""
Usage:
  program filter (in|out) (allow|deny|reject) [--interface=<iface>...] [--proto=<proto>...]
  program -h|--help

Options:
  -h|--help                 show this help text
  -i, --interface=<iface>   filter on this interface [default: eth0]
  -p, --proto=<proto>       filter on this protocol [default: tcp]
"""

from docopt import docopt
import sys
import schema

def validate_proto(protocols):
    valid_protocols = ['tcp', 'udp']
    for protocol in protocols:
        if not protocol in valid_protocols:
            err = 'Invalid protocol: [%s]. Allowed: %s' %\
                  (protocol, valid_protocols)
            raise ValueError(err)
    return True


def validate_interface(ifaces):
    valid_ifaces = ['eth0', 'eth1']
    for iface in ifaces:
        if not iface in valid_ifaces:
            err = 'Invalid interface: [%s]. Allowed: %s' %\
                  (iface, valid_ifaces)
            raise ValueError(err)
    return True

def validate_args(ds):
    validation_schema = schema.Schema({
        'interface': validate_interface,
        'protocol': validate_proto
    })
    validation_schema.validate(ds)

def load_args(args):
    parsed_docopt = docopt(__doc__, version='1.0')
    print parsed_docopt
    ds = {}
    ds['interface'] = parsed_docopt['--interface']
    ds['protocol'] = parsed_docopt['--proto']
    validate_args(ds)
    return ds

if __name__ == '__main__':
    print load_args(sys.argv[1:])
