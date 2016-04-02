### Audit manual setup

Supplments the demos in [http://saurabh-hirani.github.io/slides/monitoring-transition.html#/4](Audit manual setup) for the talk.

Assumption: icinga container running as per - [https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/icinga](icinga manual setup)

## Discover

Peek under the hood. We are just using curl calls to [https://github.com/dmytro/nagira](nagira)

```
$ ./discover-hosts-list.sh
```

```
$ ./discover-hostgroups-list.sh
```

```
$ ./discover-hosts-details.sh
```

```
$ ./discover-hostgroups-details.sh
```

```
$ ./discover-services-list.sh
```

```
$ ./discover-services-details.sh
```

## Categorize

- Now that you can discover hosts, hostgroups, checks - cateogrizing is a do-it-yourself job which varies as per the setup you have.

## Consolidate checks

[https://github.com/saurabh-hirani/fpm-docker-demo](fpm-docker-demo)
