
# prog [--version] [--help] [-c <name>=<value>] [--exec-path[=<path>]] 
# changd -c <name>=<value> to --command=<cmd_kv>
# change <git_cmd> [<args>]

"""
Usage:
  git_prog [--version] [--help] [--command=<cmd_kv>] [--exec-path=<path>] 
       [--html-path] [--man-path] [--info-path] [-p|--paginate|--no-pager] 
       [--no-replace-objects] [--bare] [--git-dir=<path>] [--work-tree=<path>] 
       [--namespace=<name>] <git_cmd> [--cmd_data=<data>]

Options:
  --exec-path=<path>  where git progs installed [default: /var/tmp/exec_path]
  --git-dir=<path>    git directory [default: /var/tmp/git_dir]
  --work-tree=<path>  work path [default: /var/tmp/work_tree]
  --namespace=<name>  namespace [default: def_namespace]
"""

add_usage = """
Usage:
   [-n] [-v] [--force] [--interactive] [--patch]
   [--edit] [--all|--update] [--intent-to-add|-N]
   [--refresh] [--ignore-errors] [--ignore-missing] [--]
   [<filepattern>...]

Options:
   -f, --force         forcefully
   -i, --interactive   interactively

"""

from docopt import docopt
import sys

def load_args(args):
    parsed_docopt = docopt(__doc__, version='1.0')
    print parsed_docopt
    print "----------\n"
    if parsed_docopt['<git_cmd>'] == 'add':
        parsed_docopt = docopt(add_usage, parsed_docopt['--cmd_data'])
        print parsed_docopt

if __name__ == '__main__':
    load_args(sys.argv[1:])
