# Copyright 2015 A10 Networks
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
import test_base
# import pdb
# import mock
import a10_neutron_lbaas.contrail.v1.v1_context as a10


class FakeException(Exception):
    pass


class TestA10Context(test_base.UnitTestBase):
    def __init__(self, *args):
        super(TestA10Context, self).__init__(*args)

    def setUp(self):
        super(TestA10Context, self).setUp()
        #import pdb
        #pdb.set_trace()
        self.handler = self.a._pool_handler
        self.m = test_base.FakePool()

    def test_context(self):
        with a10.A10Context(self.handler, self.m) as c:
            self.empty_mocks()
            c
        self.empty_close_mocks()

    def test_context_e(self):
        try:
            with a10.A10Context(self.handler, self.m) as c:
                self.empty_mocks()
                c
                raise FakeException()
        except FakeException:
            self.empty_close_mocks()

    def test_write(self):
        with a10.A10WriteContext(self.handler, self.m) as c:
            c
        self.a.last_client.system.action.write_memory.assert_called_with()
        self.a.last_client.session.close.assert_called_with()

    def test_ha(self):
        with a10.A10WriteContext(self.handler, self.m,
                                 device_name='ax4') as c:
            c
        self.a.last_client.ha.sync.assert_called_with(
            '1.1.1.1', 'admin', 'a10')
        self.a.last_client.session.close.assert_called_with()

    def test_write_e(self):
        try:
            with a10.A10WriteContext(self.handler, self.m) as c:
                c
                raise FakeException()
        except FakeException:
            self.empty_close_mocks()
            pass

    def test_write_status(self):
        with a10.A10WriteStatusContext(self.handler, self.m) as c:
            c
        # #self.a.openstack_driver._active.assert_called_with(self.get_admin_mock.return_value,
        #                                                    'pool', 'fake-id-001')
            self.a._api.loadbalancer_update_pool.assert_called_with("pool", "fake-id-001")

    def test_write_status_e(self):
        try:
            with a10.A10WriteStatusContext(self.handler,
                                           self.m) as c:
                c
                raise FakeException()
        except FakeException:
            # self.a.openstack_driver._failed.assert_called_with(self.get_admin_mock.return_value,
            #                                                    'pool', 'fake-id-001')
            pass

    def test_delete(self):
        #import pdb
	    #pdb.set_trace()
        test_pool = {"id": "fake-id-001", "name": "fake-id-001", "tenant_id": "tenant-pays-rent-on-time"}
        with a10.A10DeleteContext(self.handler, test_pool) as c:
            c
        self.a.openstack_driver._db_delete.assert_called_with(self.get_admin_mock.return_value,
                                                              'pool', 'fake-id-001')

    def test_delete_e(self):
        try:
            with a10.A10DeleteContext(self.handler, self.m) as c:
                c
                raise FakeException()
        except FakeException:
            self.empty_close_mocks()
            pass


# Re-run all the context manager tests with appliance partitioning.
class TestA10ContextADP(TestA10Context):

    def setUp(self):
        super(TestA10ContextADP, self).setUp()
        self.reset_v_method('adp')

    def tearDown(self):
        self.reset_v_method('lsi')

    def reset_v_method(self, val):
        for k, v in self.a.config.devices.items():
            v['v_method'] = val

    def empty_mocks(self):
        self.print_mocks()
        self.assertEqual(1, len(self.a.last_client.mock_calls))
        self.a.last_client.system.partition.active.assert_called_with(
            self.m['tenant_id'])

    def empty_close_mocks(self):
        self.print_mocks()
        self.assertEqual(2, len(self.a.last_client.mock_calls))
        self.a.last_client.session.close.assert_called_with()
