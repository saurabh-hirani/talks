### Audit manual setup

Assumption: icinga container running as per - [icinga manual setup](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/manual-setup)

## Discover

Peek under the hood. We are just using curl calls to [nagira](https://github.com/dmytro/nagira)

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

[fpm-docker-demo](https://github.com/saurabh-hirani/fpm-docker-demo)
