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
import v1.handler_hm
import v1.handler_member
import v1.handler_pool
import v1.handler_vip
import version

LOG = logging.getLogger(__name__)


class A10OpenstackLBV1(A10OpenstackLBBase):

    @property
    def pool(self):
        return v1.handler_pool.PoolHandler(self)

    @property
    def vip(self):
        return v1.handler_vip.VipHandler(self)

    @property
    def member(self):
        return v1.handler_member.MemberHandler(self)

    @property
    def hm(self):
        return v1.handler_hm.HealthMonitorHandler(self)
