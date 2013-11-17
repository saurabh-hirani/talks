# docopt overview

- Created by Vladimir Keleshev

- PyCon UK video - [docopt intro](http://docopt.org)

- Some code snippets taken from above site

## Command line tools

- API for your program

- Often act as a base design for developing UI

- A well defined command line program makes you program against an
  interface and not an implementation

- Sample command line: `usage.txt` 

## Parsing command line using optparse

- Not much support beyond adding options (the `--`  stuff)

- Need to write logic for subcommands

- A series of if-this-sub_command-validate-sub_command-env statements

- Program: `connector_1.py` 

## Parsing command line using argparse

- More intuitive than optparse

- Can add subparsers (sub_commands)

- Creates help usage on the fly (try doing `program sub_command help`)

- Was using this before docopt found me

- Have tried only optparse, argparse and docopt. Any other favorite 
  command line parsers?

- Program: `connector_2.py`

## Parsing command line using docopt

- Specify a POSIX complaint usage (more fun than it sounds)

- Write your doc first

- docopt takes care of the rest

- Sort of like specifying a syntax and try to fit your command line in it

- No semantic validation (e.g. is `--src_file` a valid file?) 
  - a good thing - I would rather employ my own mechanisms (more later)

- Program: `connector_3.py`

## Keep the design and development separate yet connected

- Read man page of `git` command

- Copied the synopsis, made minimal changes and added functionality to 
  support `git` and `git add`  command in less than 10 minutes.

- Keep the command line parsing work as minimal as possible

- Break it into chunks - syntactic validation, semantic validation so that
  both can be done separately

- Try writing that with argparse

- Mind. Blown.

- Program: `git_1.py`

## Validating the input

- Use `schema` module

- I find the separation of parsing and validating natural and intuitive.

- Program: `rule_filter.py` 

## Handy docopt options

- Supports a lot of interesting features e.g. specifying command line 
  switch multiple times, mandating usage of arguments in pairs, etc.

- Program: `one_liners.py`

- See module documentation for an exhaustive list

## Wrapping up

- Watch the video - [docopt intro](http://docopt.org)

- Use docopt!  
