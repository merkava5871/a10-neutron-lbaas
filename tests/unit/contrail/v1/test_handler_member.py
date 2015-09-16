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

import test_base


def return_one(*args):
    return 1


def return_two(*args):
    return 2


def _fake_member(pool_id='pool1', admin_state_up=True):
    return {
        'address': '1.1.1.1',
        'tenant_id': 'ten1',
        'id': 'id1',
        'admin_state_up': admin_state_up,
        'pool_id': pool_id,
        'protocol_port': '80',
    }.copy()


class TestMembers(test_base.UnitTestBase):

    def set_count_1(self):
        self.a._svc_mon._member_count = return_one

    def set_count_2(self):
        self.a._svc_mon._member_count = return_two

    def test_get_ip(self):
        m = self.fake_member()
        self.a.member_handler.contrail.member_get_ip(None, m, False)
        self.a._db._member_get_ip.assert_called_with(None,
            m, False)

    def test_get_name(self):
        m = self.fake_member()
        z = self.a.member_handler._get_name(m, '1.1.1.1')
        self.assertEqual(z, '_ten1_1_1_1_1_neutron')

    def test_count(self):
        self.a.member_handler.contrail.member_count(None, self.fake_member())

    def fake_member(self, pool_id='pool1', admin_state_up=True):
        return _fake_member(pool_id, admin_state_up)

    def test_create(self, admin_state_up=True):
        m = self.fake_member(admin_state_up=admin_state_up)
        ip = self.a.member_handler.contrail.member_get_ip(m, True)
        name = self.a.member_handler._get_name(m, ip)
        self.a.member_handler.create(m)

        self.a.last_client.slb.server.create.assert_called_with(
            name, ip,
            axapi_args={'server': {}})
        if admin_state_up:
            status = self.a.last_client.slb.UP
        else:
            status = self.a.last_client.slb.DOWN
        pool_name = self.a.member_handler._pool_name(m['pool_id'])
        self.a.last_client.slb.service_group.member.create.assert_called_with(
            pool_name, name, m['protocol_port'], status=status,
            axapi_args={'member': {}})

    def test_create_down(self):
        self.test_create(False)

    def test_update_down(self):
        m = self.fake_member(admin_state_up=False)
        ip = self.a.member_handler.contrail.member_get_ip(m, True)
        name = self.a.member_handler._get_name(m, ip)
        self.a.member_handler.update(m, m)

        pool_name = self.a.member_handler._pool_name(m['pool_id'])
        self.a.last_client.slb.service_group.member.update.assert_called_with(
            pool_name, name, m['protocol_port'],
            self.a.last_client.slb.DOWN,
            axapi_args={'member': {}})

    def test_delete(self):
        m = self.fake_member()
        ip = self.a.member_handler.contrail.member_get_ip(m, True)

        self.set_count_1()
        self.a.member_handler.delete(m)

        self.a.last_client.slb.server.delete(ip)

    def test_delete_count_gt_one(self):
        # import pdb
        # pdb.set_trace()
        m = self.fake_member()
        handler = self.a.member_handler
        handler.contrail.member_get_ip = (lambda x, y: "127.0.0.1")
        ip = handler.contrail.member_get_ip(m, True)
        name = handler._get_name(m, ip)
        handler.contrail.member_count = (lambda x, y: 2)
        
        self.set_count_2()
        handler.delete(m)

        pool_name = handler._pool_name(m['pool_id'])
        self.a.last_client.slb.service_group.member.delete.assert_called_with(
            pool_name, name, m['protocol_port'])
