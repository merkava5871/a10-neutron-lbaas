#! /bin/bash
# This script creates a driver in contrail's config DB based on the variables set below
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

log $VNC_CMD_BASE/service_appliance.py --api_server_ip $VNC_API_IP --api_server_port $VNC_API_PORT --oper del --admin_user $VNC_USER --admin_password $VNC_PASSWORD --admin_tenant_name $VNC_TENANT --name vthunder --service_appliance_set a10networks --device_ip $DEVICE_IP --user_credential $USER_CREDENTIAL 
