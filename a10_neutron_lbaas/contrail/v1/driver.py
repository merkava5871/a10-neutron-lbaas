# Copyright 2014, Doug Wiegley (dougwig), A10 Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from svc_monitor.services.loadbalancer.drivers import abstract_driver
from vnc_api.vnc_api import *

from a10_neutron_lbaas.contrail import a10_config
from a10_neutron_lbaas.contrail import plumbing_hooks as hooks
from a10_neutron_lbaas.contrail.v1 import handler_pool
from a10_neutron_lbaas.contrail.v1 import handler_vip
from a10_neutron_lbaas.contrail.v1 import handler_member
from a10_neutron_lbaas.contrail.v1 import handler_hm
# from a10_neutron_lbaas.contrail.v1 import v1_context as a10

LOADBALANCER_SERVICE_TEMPLATE = {
    "default-domain",
    "a10-loadbalancer-template"
}


class A10ContrailLoadBalancerDriver(abstract_driver.ContrailLoadBalancerAbstractDriver):
    def __init__(self, name, manager, api, db, args=None):
        self._name = name
        self._api = api
        self._svc_mon = manager
        self._args = args
        self.db = db
        self.config = a10_config.A10Config()
        self.plumbing_hooks = hooks.PlumbingHooks(self)
        self._lb_template = None
        self.openstack_driver = None
        self._pool_handler = handler_pool.PoolHandler(self)
        self._vip_handler = handler_vip.VipHandler(self)
        self._hm_handler = handler_hm.HealthMonitorHandler(self)
        self._member_handler = handler_member.MemberHandler(self)

    def _select_a10_device(self, tenant_id):
        return self.plumbing_hooks.select_device(tenant_id)

    def _get_template(self):
        if self._lb_template is not None:
            return
        self._lb_template = self._api.service_template_read(
            fq_name=LOADBALANCER_SERVICE_TEMPLATE)

    def _update_lb_instance(self, upool):
        pool_id = upool.get("id")
        vip_id = upool.get("id")

        try:
            pool = self._api.loadbalancer_pool_read(id=pool_id)
        except NoIdError:
            msg = ("Unable to retrieve pool %s" % pool_id)
            self._svc_manager.logger.log_error(msg)
            return

        try:
            vip = self._api.virtual_ip_read(id=vip_id)
        except NoIdError:
            msg = ("Unable to retrieve VIP %s" % vip_id)
            self._svc_manager.logger.log_error(msg)
            return

        fq_name = pool.get_fq_name()[:-1]
        fq_name.append(pool_id)

        props = service_instance._get_instance_properties(pool, vip)
        if props is None:
            try:
                self._api.service_instance_delete(fq_name=fq_name)
            except RefsExistError as ex:
                self._svc_manager.logger.log_error(str(ex))
            return

        self._get_template()

        try:
            service_instance = self._api.service_instance_read(fq_name=fq_name)
            # TODO(mmd) - This code doesn't look right.
            updated = self._service_instance_update_props(service_instance, props)
            if updated:
                self._api.service_instance_update(service_instance)
        except NoIdError:
            proj_obj = self._api.project_read(fq_name=fq_name[:-1])
            service_instance = ServiceInstance(name=fq_name[-1], parent_obj=proj_obj,
                                               service_instance_properties=props)
            service_instance.set_service_template(self._lb_template)
            self._api_service_instance_create(service_instance)

        si_refs = pool.get_service_instance_refs()
        if si_refs is None or si_refs[0].get('uuid') != service_instance.uuid:
            pool.set_service_instance(service_instance)
            self._api.loadbalancer_pool_update(pool)
        self.db.pool_driver_info_insert(pool_id, {"service_instance": service_instance.uuid})

    def _clear_lb_instance(self, pool):
        driver_data = self.db.pool_driver_info_get(pool_id)
        if driver_data is None:
            return
        si_id = driver_data['service_instance']
        try:
            service_instance = self._api.service_instance.read(id=si_id)
        except NoIdError as ex:
            self._svc_manager.logger.log_error(str(ex))
            return

        pool_back_refs = service_instance.get_loadbalancer_pool_back_refs()
        for pool_back_ref in pool_back_refs or []:
            pool_obj = self._api.loadbalancer_pool_read(
                id=pool_back_ref["uuid"])
            pool_obj.del_service_instance(service_instance)
            self._api.loadbalancer_pool_update(pool_obj)

        try:
            self._api.service_instance_delete(id=si_id)
        except RefsExistError as ex:
            sef._svc_manager.logger.log_error(str(ex))
        #  TODO(mmd) - What's up with the second param?
        self.db.pool_remove(pool_id, ['service_instance'])

    def create_vip(self, vip):
        # Check if device requires SNAT support so we can appropriately config the vip
        # Create VIP on device, check for error
        # If success, pass creation on to backend
        # If failure, set error status (INACTIVE)

        raise Exception("Not implemented")

    def update_vip(self, old_vip, vip):
        raise Exception("Not implemented")

    def delete_vip(self, vip):
        raise Exception("Not implemented")

    def create_pool(self, pool):
        # Service appliance has to exist before pool can be created
        # If service appliance can't be located, bail (and possibly raise exception)!
        # Create pool on device, check status
        # If success, pass creation to backend
        # Else, set pool status to INACTIVE and raise exception.
        self._get_template()
        try:
            if pool.get("vip_id"):
                self._update_lb_instance(pool)
        except Exception as ex:
            # TODO(mmd) - You need a logger, dude.
            return

        try:
            self.pool_handler.create(pool)
        except Exception as ex:
            # TODO(mmd) - You need a logger, dude.
            return

    def update_pool(self, old_pool, pool):
        raise Exception("Not implemented")

    def delete_pool(self, pool):
        old_pool_svc, new_pool_svc = self.locate_resources(pool['id'], False)
        if old_pool_svc:
            self.delete_service(old_pool_svc)
            self.db.pool_remove(pool['id'])
            self.pool_handler.delete(pool)

    def stats(self, pool_id):
        raise Exception("Not implemented")

    def create_member(self, member):
        raise Exception("Not implemented")

    def update_member(self, old_member, member):
        raise Exception("Not implemented")

    def delete_member(self, member):
        raise Exception("Not implemented")

    def create_pool_health_monitor(self,
                                   health_monitor,
                                   pool_id):
        raise Exception("Not implemented")

    def delete_pool_health_monitor(self, health_monitor, pool_id):
        raise Exception("Not implemented")

    def update_health_monitor(self,
                              old_health_monitor,
                              health_monitor,
                              pool_id):
        raise Exception("Not implemented")

    @property
    def pool_handler(self):
        return self._pool_handler

    @property
    def vip_handler(self):
        return self._vip_handler

    @property
    def member_handler(self):
        return self._member_handler

    @property
    def monitor_handler(self):
        return self._hm_handler
