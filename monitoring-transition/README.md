#### Title
The transition: Manual => Automated => Distributed monitoring

#### Objective
Everyone talks the benefits of having an automated monitoring system in place - one which can discover
infrastructure components as they are added, monitor them while they are alive and stop monitoring when
they are moved out. But no one has chronicled their journey through the process of automating a manually
maintained monitoring system and showcased their battle scars for others to learn from. That's what
we are going to talk about.

#### Description
We moved our monitoring systems from a manually maintained nagios setup to an automated, distributed  
icinga2 infrastructure. This talk is going to cover the following topics:

- The challenges of monitoring a distributed infrastructure
- A manually maintained nagios setup and its limitations
- Prepping for moving to an automated icinga2 setup
- Collating data from multiple host sources
- Progressive cutover from manual to automated monitoring

#### Slides

- http://saurabh-hirani.github.io/slides/monitoring-transition.html#/

#### Talk

- TODO

#### Setup

- TODO

#### Host discovery in the manual setup

- Start icinga docker image

```
$ docker run --privileged=true -p 8080:80 -p 4567:4567 -p 6315:6315  -v /data/icinga:/shared -i -t shirani/icinga-demo /bin/bash
```

- Start nagira in docker

```
$ RACK_ENV=production nagira
```

- Test nagira on host

```
# get list of hosts
$ curl http://localhost:4567/_objects/hosts/_list | python -m json.tool | less

# get detailed status of all hosts
$ curl http://localhost:4567/_objects/hosts/_full | python -m json.tool | less

# get list of services
$ curl http://localhost:4567/_objects/services/_list | python -m json.tool | less

# get detailed status of all services
$ curl http://localhost:4567/_objects/services/_full | python -m json.tool | less
```

- Start nagios-api in docker

```
$ nagios-api  -s /var/lib/icinga/status.dat -p 6315 -c /var/lib/icinga/rw/icinga.cmd
```

- Test nagios-api on host

```
$ curl http://localhost:6315/state
```

#### Consolidate server side checks

- jsonalyzer - https://github.com/saurabh-hirani/jsonalyzer

- fpm - https://github.com/saurabh-hirani/fpm-docker-demo


#### Parallel setup

- TODO

#### Progressive cutover

- TODO
