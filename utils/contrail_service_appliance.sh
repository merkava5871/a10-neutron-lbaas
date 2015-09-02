#! /bin/bash
VNC_CMD_BASE=/opt/stack/contrail/controller/src/config/utils
VNC_TENANT_NAME=admin
VNC_USER=admin
VNC_PASSWORD=contrail123
VNC_API_IP=127.0.0.1
VNC_API_PORT=8082
DRIVER_NAME=a10networks
DRIVER_PATH=a10_neutron_lbaas.contrail.v1.driver.A10ContrailLoadBalancerDriver
DRIVER_PROPERTIES='{"config_path": "/etc/a10/config.py"}'

echo $VNC_CMD_BASE/service_appliance_set.py --api_server_ip $VNC_API_IP --api_server_port $VNC_API_PORT --oper add --admin_user $VNC_USER --admin_password $VNC_PASSWORD --admin_tenant_name $VNC_TENANT --name a10networks --driver "$DRIVER_PATH" --properties \'$DRIVER_PROPERTIES\'
