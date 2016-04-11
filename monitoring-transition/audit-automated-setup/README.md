## Audit automated setup

### Assumptions: 

  - icinga2 VM running as per - [icinga2 automated setup](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/automated-setup/icinga2_monitor)

### Generated host configs from inventories

  - [configure_*_nodes.rb recipes](https://github.com/saurabh-hirani/talks/tree/master/monitoring-transition/automated-setup/icinga2_monitor/recipes)

### Decoupled check configs

  - [configure_checks.rb](https://github.com/saurabh-hirani/talks/blob/master/monitoring-transition/automated-setup/icinga2_monitor/recipes/configure_checks.rb)

### CRUD API

Peek under the hood. We are just calling [icinga2_api](https://github.com/saurabh-hirani/icinga2_api)

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
