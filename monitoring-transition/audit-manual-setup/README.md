### Audit manual setup

Assumption: icinga container running as per - [icinga manual setup](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/manual-setup)

## Discover

Peek under the hood. We are just using curl calls to [nagira](https://github.com/dmytro/nagira)

```
$ ./discover-hosts-list
```

```
$ ./discover-hosts-details
```

```
$ ./discover-hostgroups-list
```

```
$ ./discover-hostgroups-details
```

```
$ ./discover-services-details
```

## Categorize

- Now that you can discover hosts, hostgroups, checks - cateogrizing is a do-it-yourself job which varies as per the setup you have.
