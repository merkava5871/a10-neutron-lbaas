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

import acos_client.errors as acos_errors
import handler_base_v1
import v1_context as a10


class MemberHandler(handler_base_v1.HandlerBaseV1):

    def _get_name(self, member, ip_address):
        tenant_label = member['tenant_id'][:5]
        addr_label = str(ip_address).replace(".", "_", 4)
        server_name = "_%s_%s_neutron" % (tenant_label, addr_label)
        return server_name

    def _meta_name(self, member, ip_address):
        return self.meta(member, 'name', self._get_name(member, ip_address))

    def _create(self, c, member):
        server_ip = self.neutron.member_get_ip(member,
                                               c.device_cfg['use_float'])
        server_name = self._meta_name(member, server_ip)

        status = c.client.slb.UP
        if not member['admin_state_up']:
            status = c.client.slb.DOWN

        try:
            server_args = {'server': self.meta(member, 'server', {})}
            c.client.slb.server.create(server_name, server_ip,
                                       axapi_args=server_args)
        except (acos_errors.Exists, acos_errors.AddressSpecifiedIsInUse):
            pass

        try:
            member_args = {'member': self.meta(member, 'member', {})}
            c.client.slb.service_group.member.create(
                self._pool_name(member['pool_id']),
                server_name,
                member['protocol_port'],
                status=status,
                axapi_args=member_args)
        except acos_errors.Exists:
            pass

    def create(self, member):
        with a10.A10WriteStatusContext(self, member) as c:
            self._create(c, member)
            self.hooks.after_member_create(c, member)

    def update(self, old_member, member):
        with a10.A10WriteStatusContext(self, member) as c:
            server_ip = self.neutron.member_get_ip(member,
                                                   c.device_cfg['use_float'])
            server_name = self._meta_name(member, server_ip)

            status = c.client.slb.UP
            if not member['admin_state_up']:
                status = c.client.slb.DOWN

            try:
                member_args = {'member': self.meta(member, 'member', {})}
                c.client.slb.service_group.member.update(
                    self._pool_name(member['pool_id']),
                    server_name,
                    member['protocol_port'],
                    status,
                    axapi_args=member_args)
            except acos_errors.NotFound:
                # Adding db relation after the fact
                self._create(c, member)

            self.hooks.after_member_update(c, member)

    def _delete(self, c, member):
        # TODO(teamvnc) - replace with call to contrail ops.
        server_ip = "127.0.0.1"
        server_name = self._meta_name(member, server_ip)

        try:
            if self.neutron.member_count(member) > 1:
                c.client.slb.service_group.member.delete(
                    self._pool_name(member['pool_id']),
                    server_name,
                    member['protocol_port'])
            else:
                c.client.slb.server.delete(server_name)
        except acos_errors.NotFound:
            pass

        self.hooks.after_member_delete(c, member)

    def delete(self, member):
        with a10.A10DeleteContext(self, member) as c:
            self._delete(c, member)
