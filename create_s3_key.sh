#!/bin/sh

token=`openstack token issue|grep "| id"|awk -F '|' '{print $3}'`
userid=$1
tenantid=$2

curl -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $token" http://KEYSTONE_AUTH_SERVER:35357/v3/users/$1/credentials/OS-EC2 -d '{"tenant_id": "$2"}'
