# Copyright 2015,  A10 Networks
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
#    under the License.from neutron.db import model_base

import mock

import a10_neutron_lbaas.tests.db.test_base as test_base

import a10_neutron_lbaas.db.operations as db_operations
import a10_neutron_lbaas.v2.inventory as inventory


class TestInventory(test_base.UnitTestBase):

    def inventory(self):
        session = self.open_session()
        operations = db_operations.Operations(mock.MagicMock(session=session))

        a10_context = mock.MagicMock(
            db_operations=operations,
            openstack_context=mock.MagicMock(session=session))

        return inventory.InventoryV2(a10_context)

    def test_find_selects_appliance(self):
        target = self.inventory()
        appliance = target.db_operations.summon_appliance_configured('fake-device-key')
        target.a10_context.a10_driver._select_a10_device.return_value = {'key': 'fake-device-key'}

        openstack_lbaas_object = mock.MagicMock(root_loadbalancer=mock.MagicMock(id='fake-lb-id'))
        found_appliance = target.find(openstack_lbaas_object)

        self.assertEqual(appliance, found_appliance)

    def test_find_creates_slb(self):
        target = self.inventory()
        appliance = target.db_operations.summon_appliance_configured('fake-device-key')
        target.a10_context.a10_driver._select_a10_device.return_value = {'key': 'fake-device-key'}

        openstack_lbaas_object = mock.MagicMock(root_loadbalancer=mock.MagicMock(id='fake-lb-id'))
        target.find(openstack_lbaas_object)

        slb = target.db_operations.get_slb_v2('fake-lb-id')

        self.assertEqual(appliance, slb.a10_appliance)

    def test_find_finds_slb(self):
        target1 = self.inventory()
        target1.a10_context.a10_driver._select_a10_device.return_value = {'key': 'fake-device-key'}

        openstack_lbaas_object = mock.MagicMock(root_loadbalancer=mock.MagicMock(id='fake-lb-id'))
        target1.find(openstack_lbaas_object)
        target1.db_operations.session.commit()

        target2 = self.inventory()
        found_appliance = target2.find(openstack_lbaas_object)

        self.assertEqual('fake-device-key', found_appliance.device_key)