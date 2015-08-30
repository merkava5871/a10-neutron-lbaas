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

import a10_config
from a10_openstack_lb_base import A10OpenstackLBBase
import acos_client
import plumbing_hooks as hooks
import v2.handler_hm
import v2.handler_lb
import v2.handler_listener
import v2.handler_member
import v2.handler_pool
import version

LOG = logging.getLogger(__name__)


class A10OpenstackLBV2(A10OpenstackLBBase):

    @property
    def lb(self):
        return v2.handler_lb.LoadbalancerHandler(
            self,
            self.openstack_driver.load_balancer,
            neutron=self.neutron)

    @property
    def loadbalancer(self):
        return self.lb

    @property
    def listener(self):
        return v2.handler_listener.ListenerHandler(
            self,
            self.openstack_driver.listener,
            neutron=self.neutron,
            barbican_client=self.barbican_client)

    @property
    def pool(self):
        return v2.handler_pool.PoolHandler(
            self, self.openstack_driver.pool,
            neutron=self.neutron)

    @property
    def member(self):
        return v2.handler_member.MemberHandler(
            self,
            self.openstack_driver.member,
            neutron=self.neutron)

    @property
    def hm(self):
        return v2.handler_hm.HealthMonitorHandler(
            self,
            self.openstack_driver.health_monitor,
            neutron=self.neutron)

