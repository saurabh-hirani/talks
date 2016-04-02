#!/bin/bash
echo "starting nagira"
RACK_ENV=production nagira > /var/log/nagira.log 2>&1 &
