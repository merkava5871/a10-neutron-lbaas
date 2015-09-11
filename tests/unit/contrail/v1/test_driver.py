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


from mock import Mock,MagicMock
import tests.unit.contrail.test_base as test_base
import uuid
from a10_neutron_lbaas.contrail.v1 import driver as a10_vnc

class TestA10ContrailLoadBalancerDriver(test_base.UnitTestBase):
    def _build_fake_pool(self):
        return {
            "name": "lb-name",
            "id": str(uuid.uuid4()),
            "vip_id": str(uuid.uuid4())
        }

    def setUp(self):
        super(TestA10ContrailLoadBalancerDriver, self).setUp()
        self.target = a10_vnc.A10ContrailLoadBalancerDriver("lb-name", Mock(), Mock(), Mock(), {})
        self.fake_pool = self._build_fake_pool()

    def test_create_pool_calls_pool_handler(self):
        self.target.create_pool(self.fake_pool)
        self.assertEqual(1, self.target.pool_handler.create.call_count)

    def test_create_pool_calls_backend_handler(self):
        self.target.create_pool(self.fake_pool)
        self.assertEqual(1, self.target.db.pool_driver_info_insert.call_count)
