#! /bin/bash

# List networks - if we can't do this, see ya
source test-context.sh
NETWORK=(neutron net-list | awk { print $2 })


