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

import mock
from mock import Mock

import sys

with mock.patch.dict(sys.modules,
                     {
                         "a10_neutron_lbaas.contrail.a10_openstack_lb": Mock(),
                         "a10_neutron_lbaas.contrail.v1.handler_base_v1": Mock(),
                         "a10_neutron_lbaas.contrail.v1.handler_pool.PoolHandler": Mock(),
                         "a10_neutron_lbaas.contrail.v1.handler_member": Mock(),
                         "a10_neutron_lbaas.contrail.v1.handler_vip": Mock(),
                         "a10_neutron_lbaas.contrail.v1.handler_hm": Mock(),
                     }
                     ):
    pass
    # from a10_neutron_lbaas.contrail.v1 import handler_base_v1
    # from a10_neutron_lbaas.contrail.v1 import handler_pool
    # from a10_neutron_lbaas.contrail.v1 import handler_member
    # from a10_neutron_lbaas.contrail.v1 import handler_vip
    # from a10_neutron_lbaas.contrail.v1 import handler_hm


import tests.unit.contrail.test_base as test_base



class UnitTestBase(test_base.UnitTestBase):
    def __init__(self, *args):
        super(UnitTestBase, self).__init__(*args)
        self.get_admin_patch = mock.patch("neutron.context.get_admin_context")
        self.get_admin_mock = self.get_admin_patch.start()

        self.version = 'v1'
