#! /bin/bash
# This script creates a driver in contrail's config DB based on the variables set below
source 

log $VNC_CMD_BASE/service_appliance.py --api_server_ip $VNC_API_IP --api_server_port $VNC_API_PORT --oper add --admin_user $VNC_USER --admin_password $VNC_PASSWORD --admin_tenant_name $VNC_TENANT --name vthunder --service_appliance_set a10networks --device_ip $DEVICE_IP --user_credential $USER_CREDENTIAL 
