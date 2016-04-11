## Progressive cutover

### Assumptions:
  - Your [manual](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/audit-manual-setup) and [automated](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/audit-automated-setup) is up and running

### Enable notifications on new:

Peek under the hood. We are using 

- [nagios-api](https://github.com/zorkian/nagios-api) and [nagira](https://github.com/dmytro/nagira) for icinga (nagira works best for read-only, nagios-api for write operations)
- [icinga2_api](https://github.com/saurabh-hirani/icinga2_api) for icinga2

```
$ ./manage-icinga2-notifs-by-hostgroup enable app
```

### Disable notifications on old:

```
$ ./manage-icinga-notifs-by-hostgroup disable app
```

### Rinse, repeat

```
$ ./manage-icinga2-notifs-by-hostgroup enable infra
$ ./manage-icinga-notifs-by-hostgroup disable infra
```

### Enable all notifications on new:

```
$ ./enable-icinga2-notifications
```

### Rollback

```
$ ./rollback
```
