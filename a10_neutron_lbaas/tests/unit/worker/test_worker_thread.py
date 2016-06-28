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
import time
import test_base


class TestWorker(test_base.UnitTestBase):

    def _test_create(self, admin_state_up=True, uuid_name=False):
        if uuid_name:
            old = self.a.config.get('member_name_use_uuid')
            self.a.config._config.member_name_use_uuid = True

        m = test_base.FakeMember(admin_state_up=admin_state_up,
                                 pool=mock.MagicMock())
        ip = self.a.member.neutron.member_get_ip(None, m, True)
        if uuid_name:
            name = m.id
        else:
            name = self.a.member._get_name(m, ip)
        self.a.member.create(None, m)

        if admin_state_up:
            status = self.a.last_client.slb.UP
        else:
            status = self.a.last_client.slb.DOWN
        self.a.last_client.slb.server.create.assert_called_with(
            name, ip,
            status=status,
            axapi_args={'server': {}})
        self.a.last_client.slb.service_group.member.create.assert_called_with(
            m.pool.id, name, m.protocol_port, status=status,
            axapi_args={'member': {}})
        if uuid_name:
            self.a.config._config.member_name_use_uuid = old

    def test_create(self, admin_state_up=True):
        self._test_create()
        self.print_mocks()
        asdf

