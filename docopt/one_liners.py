from docopt import docopt 
from docopt import DocoptExit

def try_docopt(usg, cmd, desc = ''):
    print "\n"
    try:
        print '---(%s)---' % desc
        print "cmd: (%s)" % cmd
        print docopt(usg, cmd)
        print '---(%s)---' % desc
        print "\n"
    except DocoptExit:
        print '(%s) - failed' % cmd
    
if __name__ == '__main__':
    desc = 'one mandatory'
    usg = """
    Usage:
        my_program go (--up | --down | --left | --right)
    """
    cmd = 'go --up'
    try_docopt(usg, cmd, desc)

    cmd = 'go'
    try_docopt(usg, cmd, desc)
    
    desc = 'none mandatory'
    usg = """
    Usage:
        my_program go [--up | --down | --left | --right]
    """
    cmd = 'go'
    try_docopt(usg, cmd, desc)

    desc = 'different commands'
    usg = """
    Usage:
        my_program run [--fast]
        my_program jump [--high]
    """
    cmd = 'run'
    try_docopt(usg, cmd, desc)

    cmd = 'run --high'
    try_docopt(usg, cmd, desc)

    cmd = 'run --fast'
    try_docopt(usg, cmd, desc)

    desc = 'args occur in pairs'
    usg = """
    Usage:
        my_program move (<from> <to>)
    """
    cmd = 'move f1'
    try_docopt(usg, cmd, desc)

    cmd = 'move f1 f2'
    try_docopt(usg, cmd, desc)

    cmd = 'move f1 f2 f3'
    try_docopt(usg, cmd, desc)

    desc = 'one or more args'
    usg = """
    Usage:
        my_program <file>...
    """
    cmd = 'f1 f2 f3 f4'
    try_docopt(usg, cmd, desc)

    desc = 'two or more args'
    usg = """
    Usage:
        my_program <file> <file>...
    """
    cmd = 'f1'
    try_docopt(usg, cmd, desc)

    cmd = 'f1 f2'
    try_docopt(usg, cmd, desc)
