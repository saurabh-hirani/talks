#!/bin/bash
icinga2_api -p vagrant -u /v1/objects/hostgroups -d '{"attrs": ["name"]}'
