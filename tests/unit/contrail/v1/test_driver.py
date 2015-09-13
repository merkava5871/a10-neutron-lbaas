# Copyright 2015, A10 Networks
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

import sys
import mock
from mock import MagicMock

# with mock.patch.dict(sys.modules, {"a10_neutron_lbaas": MagicMock()}):
#     from a10_neutron_lbaas import contrail

import tests.unit.contrail.test_base as test_base
import uuid

# We should be able to do this with mock's patch method.
# Why that doesn't work is unknown to me.


from a10_neutron_lbaas.contrail.v1 import driver as a10_vnc


class MixDict(dict, object):
    def __init__(self, init_dict={}):
        self.dict = init_dict


class FakePool(dict, object):
    def __init__(self, name="lb-name", id=str(uuid.uuid4()), vip_id=str(uuid.uuid4())):
        self.name = name
        self.id = id
        self.vip_id = vip_id

        def get_fq_name(self):
            return {"default-project", "other-stuff", self.name, "loadbalancer"}


class FakeVip(dict, object):
    def __init__(self, id=str(uuid.uuid4())):
        self.id = id


class TestA10ContrailLoadBalancerDriver(test_base.UnitTestBase):
    def setUp(self):
        v1context_patcher = mock.patch('a10_neutron_lbaas.contrail.v1.v1_context')
        # phandler_patcher = mock.patch('a10_neutron_lbaas.contrail.v1.handler_pool')

        self._name = "lb-name"
        self._svc_mon = MagicMock()
        self._api = MagicMock()
        self._api.servi
        self.db = MagicMock()

        self.fake_vip = FakeVip()
        self.fake_pool = FakePool(vip_id=self.fake_vip.id)

        self.v1_context = v1context_patcher.start()
        # self.phandler = phandler_patcher.start()

        self._api.loadbalancer_pool_read.return_value = self.fake_pool
        self._api.virtual_ip_read.return_value = self.fake_vip

        self.target = a10_vnc.A10ContrailLoadBalancerDriver("lb-name", self._svc_mon,
                                                            self._api, self.db, {})
        self.target.openstack_driver = MagicMock()
        self.target._pool_handler = MagicMock()
        self.target._vip_handler = MagicMock()
        self.target._hm_handler = MagicMock()
        self.target._member_handler = MagicMock()
        super(TestA10ContrailLoadBalancerDriver, self).setUp()

    def test_pool_handler_not_null(self):
        self.assertNotEqual(None, self.target.pool_handler)

    def test_create_pool_calls_pool_handler(self):
        self.target.create_pool(self.fake_pool)
        self.assertEqual(1, self.target.pool_handler.create.call_count)

    def test_create_pool_calls_pool_handler_with_args(self):
        self.target.create_pool(self.fake_pool)
        self.assertTrue(self.target.pool_handler.create.assert_called_with(self.target, mock.ANY))

    def test_create_pool_calls_backend_handler(self):
        self.target.create_pool(self.fake_pool)
        self.assertEqual(1, self.target.db.pool_driver_info_insert.call_count)
