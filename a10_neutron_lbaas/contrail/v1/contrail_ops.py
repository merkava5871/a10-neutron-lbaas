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


class ContrailOpsV1(object):

    def __init__(self, handler):
        self.openstack_driver = handler.openstack_driver
        self.plugin = self.openstack_driver.plugin

    def hm_binding_count(self, hm_id):
        # return self.openstack_driver._hm_binding_count(context, hm_id)
        return 0

    def hm_get(self, hm_id):
        # return self.openstack_driver._pool_get_hm(context, hm_id)
        return {}

    def member_get_ip(self, member, use_float=False):
        # return self.openstack_driver._member_get_ip(context, member, use_float)
        return {}

    def member_count(self, member):
        # return self.openstack_driver._member_count(context, member)
        return 0

    def member_get(self, member_id):
        # return self.openstack_driver._member_get(context, member_id)
        return {
            "id": member_id
        }

    def pool_get(self, pool_id):
        # return self.plugin.get_pool(context, pool_id)
        return {"id" : pool_id}

    def pool_get_tenant_id(self, pool_id):
        # return self.openstack_driver._pool_get_tenant_id(context, pool_id)
        return {}

    def vip_get(self, vip_id):
        # return self.plugin.get_vip(context, vip_id)
        return {}

    def vip_get_id(self, pool_id):
        #return self.openstack_driver._pool_get_vip_id(context, pool_id)
        return {}