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


class TestHM(test_base.UnitTestBase):

    def assert_hm(self, mon_type, method, url, expect_code):
        self.print_mocks()
        self.a.last_client.slb.hm.create.assert_called_with(
            'abcdef', mon_type, '5', 5, '5',
            url=url, method=method, expect_code=expect_code,
            axapi_args={})

    def fake_hm(self, type):
        hm = {
            'tenant_id': 'tenv1',
            'id': 'abcdef',
            'type': type,
            'delay': '5',
            'timeout': 5,
            'max_retries': '5',
            'pools': [],
        }
        if type in ['HTTP', 'HTTPS']:
            hm['http_method'] = 'GET'
            hm['url_path'] = '/'
            hm['expected_codes'] = '200'
        return hm.copy()

    def test_create_ping(self):
        pool_id = "p01"
        self.a.hm.create(self.fake_hm('PING'), pool_id)
        self.assert_hm(self.a.last_client.slb.hm.ICMP, None, None, None)
        self.a.hm._pool_name(pool_id)
        self.a.last_client.slb.service_group.update.assert_called_with(
            pool_id, health_monitor='abcdef')

    def test_create_tcp(self):
        hm = self.fake_hm('TCP')
        hm['pools'] = [{'pool_id': 'p02'}, {'pool_id': 'p01'}]
        self.a.hm.create(hm, 'p01')
        self.assert_hm(self.a.last_client.slb.hm.TCP, None, None, None)
        pool_name = self.a.hm._pool_name('p02')
        self.a.last_client.slb.service_group.update.assert_called_with(
            pool_name, health_monitor='abcdef')

    def test_create_http(self):
        hm = self.fake_hm('HTTP')
        handler = self.a.hm
        pool_id = "p01"
        handler.create(hm, pool_id)
        self.assert_hm(self.a.last_client.slb.hm.HTTP, 'GET', '/', '200')

        handler._pool_name(pool_id)
        self.a.last_client.slb.service_group.update.assert_called_with(
            pool_id, health_monitor='abcdef')

    def test_create_https(self):
        handler = self.a.hm

        pool_id = "p01"

        handler.create(self.fake_hm('HTTPS'), pool_id)
        self.assert_hm(self.a.last_client.slb.hm.HTTPS, 'GET', '/', '200')
        handler._pool_name('p01')
        self.a.last_client.slb.service_group.update.assert_called_with(
            pool_id, health_monitor='abcdef')

    def test_update_tcp(self, m_old=None, m=None):
        if m_old is None:
            m_old = self.fake_hm('TCP')
        if m is None:
            m = self.fake_hm('TCP')
        m['delay'] = 20
        self.a.hm.update(m_old, m, 'p01')
        self.a.last_client.slb.hm.update.assert_called_with(
            'abcdef',
            self.a.last_client.slb.hm.TCP, 20, 5, '5',
            url=None, method=None, expect_code=None,
            axapi_args={})

    def test_delete(self):
        pool_id = "p01"
        self.a.hm.delete(self.fake_hm('HTTP'), pool_id)
        self.a.hm._pool_name(pool_id)
        self.a.last_client.slb.service_group.update.assert_called_with(
            pool_id, health_monitor='')
