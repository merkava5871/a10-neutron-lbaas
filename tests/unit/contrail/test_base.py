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

import os
import unittest
import sys

import mock
from mock import MagicMock


from a10_neutron_lbaas.contrail import a10_config as a10_config
import a10_neutron_lbaas.contrail.v1.driver as a10_vnc
import a10_neutron_lbaas.contrail.plumbing_hooks as hooks


class FakeA10ContrailLoadBalancerDriver(a10_vnc.A10ContrailLoadBalancerDriver):

    def __init__(self, name, manager, api, db, args=None):
        self.config = a10_config.A10Config()
        self.plumbing_hooks = MagicMock()
        # self.openstack_driver = MagicMock()
        self.device_info = {
            "name": "ax1",
            "host": "10.10.100.20",
            "port": 8443,
            "protocol": "https",
            "username": "admin",
            "password": "a10",
            "status": True,
            "autosnat": True,
            "api_version": "2.1",
            "v_method": "LSI",
            "max_instance": 5000,
            "use_float": True,
            "method": "hash"
        }
        self.name = name
        self.reset_mocks()
        super(FakeA10ContrailLoadBalancerDriver, self).__init__(name, manager, api, db, args)
        self._contrail_ops = mock.Mock()

    def _verify_appliances(self):
        return True

    def _get_a10_client(self, device_info):
        self.device_info = device_info
        self.last_client = mock.MagicMock()
        return self.last_client

    def reset_mocks(self):
        self.last_client = self._get_a10_client(self.device_info)
        return self.last_client

    @property
    def pool_handler(self):
        return self._pool_handler

    @property
    def member_handler(self):
        return self._member_handler

    @property
    def monitor_handler(self):
        return self._hm_handler

    @property
    def vip_handler(self):
        return self._vip_handler


class UnitTestBase(unittest.TestCase):

    def setUp(self):
        unit_dir = os.path.dirname(__file__)
        unit_config = os.path.join(unit_dir, "unit_config")
        os.environ['A10_CONFIG_DIR'] = unit_config
        self.mock_manager = MagicMock()
        self.mock_api = MagicMock()
        self.mock_db = MagicMock()
        self.mock_args = {}
        self.a = FakeA10ContrailLoadBalancerDriver("lb-unit-test", self.mock_manager, self.mock_api,
                                                   self.mock_db, self.mock_args)
       

    def print_mocks(self):
        print("CLIENT ", self.a.last_client.mock_calls)

    def empty_mocks(self):
        self.print_mocks()
        self.assertEqual(0, len(self.a.last_client.mock_calls))

    def empty_close_mocks(self):
        self.print_mocks()
        self.assertEqual(1, len(self.a.last_client.mock_calls))
        self.a.last_client.session.close.assert_called_with()
