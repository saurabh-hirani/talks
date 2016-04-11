### Test automated setup

##Assumptions: 

  - icinga2 VM running as per - [icinga2 automated setup](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/automated-setup/icinga2_monitor)
  - [icinga2_api](https://github.com/saurabh-hirani/icinga2_api) installed and setup for the **vagrant** profile in ~/.icinga2/api.yml

## Discover

Peek under the hood. We are just calling [icinga2_api](https://github.com/saurabh-hirani/icinga2_api)

```
$ ./test-api.sh
```

```
$ ./discover-hosts-list.sh
```

```
$ ./discover-hosts-details.sh
```

```
$ ./discover-hostgroups-list.sh
```

```
$ ./discover-hostgroups-details.sh
```

```
$ ./discover-services-details.sh
```
