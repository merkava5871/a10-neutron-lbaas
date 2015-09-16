#! /bin/bash
# This script contains variables and functions common to all contrail util scripts 
VNC_CMD_BASE=/opt/stack/contrail/controller/src/config/utils
VNC_TENANT=admin
VNC_USER=admin
VNC_PASSWORD=contrail123
VNC_API_IP=127.0.0.1
VNC_API_PORT=8082
DRIVER_NAME=a10networks
DRIVER_PATH=a10_neutron_lbaas.contrail.v1.driver.A10ContrailLoadBalancerDriver
DRIVER_PROPERTIES='{}'
USER_CREDENTIAL="'{\"user\": \"$VNC_USER\", \"password\": \"$VNC_PASSWORD\"}'"
DEVICE_IP=10.48.5.219

function log { 
	cmd=$*
        echo $cmd
	`$cmd`
}

function get_script_dir {
   $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
}              
