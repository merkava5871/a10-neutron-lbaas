#! /bin/bash

# List networks - if we can't do this, see ya
NETWORK_NAME="private"
source test-context.sh
NETWORK=$(neutron net-list |grep $NETWORK_NAME | awk '{ print $2 }')
echo Private network id: $NETWORK
