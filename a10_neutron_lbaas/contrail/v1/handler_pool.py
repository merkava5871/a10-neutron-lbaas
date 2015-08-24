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

import logging

from a10_neutron_lbaas import a10_openstack_map as a10_os
import acos_client.errors as acos_errors
import a10_neutron_lbaas.contrail.v1.handler_base_v1 as handler_base_v1
import a10_neutron_lbaas.contrail.v1.v1_context as a10

LOG = logging.getLogger(__name__)


class PoolHandler(handler_base_v1.HandlerBaseV1):
    def _set(self, set_method, c, pool):
        args = {'service_group': self.meta(pool, 'service_group', {})}

        set_method(
            self._meta_name(pool),
            protocol=a10_os.service_group_protocol(c, pool['protocol']),
            lb_method=a10_os.service_group_lb_method(c, pool['lb_method']),
            axapi_args=args)

    def create(self, pool):
        with a10.A10WriteStatusContext(self, pool) as c:
            try:
                self._set(c.client.slb.service_group.create,
                          c, pool)
            except acos_errors.Exists:
                pass

    def update(self, old_pool, pool):
        with a10.A10WriteStatusContext(self, pool) as c:
            self._set(c.client.slb.service_group.update,
                      c, pool)

    def delete(self, pool):
        with a10.A10DeleteContext(self, pool) as c:
            for member in pool['members']:
                # TODO(teamvnc) - replace with call to contrail ops.
                # m = self.neutron.member_get(member)
                m = self.contrail.member_get(c.openstack_context, member)
                self.a10_driver.member._delete(c, m)

            for hm in pool['health_monitors_status']:
                # TODO(teamvnc) - replace with call to contrail ops.
                z = self.contrail.hm_get(c.openstack_context, hm['monitor_id'])
                self.a10_driver.hm._delete(c, z)

            if 'vip_id' in pool and pool['vip_id'] is not None:
                # TODO(teamvnc) - replace with call to contrail ops.
                vip = self.contrail.vip_get(pool['vip_id'])
                self.a10_driver.vip._delete(c, vip)

            c.client.slb.service_group.delete(self._meta_name(pool))

    def stats(self, pool_id):
        tenant_id = self.contrail.pool_get_tenant_id(pool_id)
        pool = {'id': pool_id, 'tenant_id': tenant_id}
        with a10.A10Context(self, pool) as c:
            try:
                vip_id = self.contrail.vip_get_id(c.openstack_context, pool['id'])
                vip = self.contrail.vip_get(c.openstack_context, vip_id)
                name = self.meta(vip, 'vip_name', vip['id'])
                r = c.client.slb.virtual_server.stats(name)
                return {
                    "bytes_in": r["virtual_server_stat"]["req_bytes"],
                    "bytes_out": r["virtual_server_stat"]["resp_bytes"],
                    "active_connections":
                        r["virtual_server_stat"]["cur_conns"],
                    "total_connections": r["virtual_server_stat"]["tot_conns"]
                }
            except Exception:
                return {
                    "bytes_in": 0,
                    "bytes_out": 0,
                    "active_connections": 0,
                    "total_connections": 0
                }
