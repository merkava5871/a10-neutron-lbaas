#! /bin/bash
# This script creates a driver in contrail's config DB based on the variables set below
VNC_CMD_BASE=/opt/stack/contrail/controller/src/config/utils
VNC_TENANT=admin
VNC_USER=admin
VNC_PASSWORD=contrail123
VNC_API_IP=127.0.0.1
VNC_API_PORT=8082
DRIVER_NAME=a10networks
DRIVER_PATH=a10_neutron_lbaas.A10ContrailDriverV1
DRIVER_PROPERTIES='{}'

function log { 
	cmd=$*
        echo $cmd
	eval $cmd
}              

log $VNC_CMD_BASE/service_appliance_set.py --api_server_ip $VNC_API_IP --api_server_port $VNC_API_PORT --oper add --admin_user $VNC_USER --admin_password $VNC_PASSWORD --admin_tenant_name $VNC_TENANT --name a10networks --driver $DRIVER_PATH
