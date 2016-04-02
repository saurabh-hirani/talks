### Audit manual setup

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

## Consolidate checks

[https://github.com/saurabh-hirani/fpm-docker-demo](fpm-docker-demo)
