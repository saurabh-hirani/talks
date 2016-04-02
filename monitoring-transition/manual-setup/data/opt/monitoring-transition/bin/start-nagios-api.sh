#!/bin/bash
if [ -f /var/run/nagios-api.pid ]; then
  rm /var/run/nagios-api.pid
fi
echo "starting nagios-api"
nagios-api  -s /var/lib/icinga/status.dat -p 6315 -c /var/lib/icinga/rw/icinga.cmd > /var/log/nagios-api.log 2>&1 &
