#!/bin/sh

export FORWARDED_ALLOW_IPS=$(getent hosts caddy | awk '{ print $1 }')

exec "$@"
