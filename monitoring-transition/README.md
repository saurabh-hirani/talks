#### The transition: Manual => Automated => Distributed monitoring

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
- Working with development teams for service healthstatus monitoring
- Progressive cutover from manual to automated monitoring
