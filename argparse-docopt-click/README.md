### argparse-docopt-click

This talk compares building the command line interface for a [sampletodo](https://github.com/saurabh-hirani/sampletodo) app using [argparse](https://docs.python.org/2.7/library/argparse.html), [docopt](http://docopt.org/) and [click](http://click.pocoo.org/5/)

### Slides

- Powered by the [go present](https://godoc.org/golang.org/x/tools/present) tool
- [Here](https://github.com/saurabh-hirani/talks/tree/master/argparse-docopt-click/slides)

### Local setup

```
# cd code
# sudo pip install pipenv
# sudo pipenv install -r requirements.txt
# sudo pipenv shell
```

### Code

- [Here](https://github.com/saurabh-hirani/talks/tree/master/argparse-docopt-click/code)

### Run tests

- Ensure that ```pipenv``` setup is done

- Run test for each implementation:
```
# ./test.sh docopt 2>&1 | less
# ./test.sh argparse 2>&1 | less
# ./test.sh click 2>&1 | less
```

