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

import logging

import a10_neutron_lbaas.a10_exceptions as a10_ex
import a10_neutron_lbaas.a10_openstack_map as a10_os

import acos_client.errors as acos_errors
import a10_neutron_lbaas.contrail.v1.handler_base_v1 as handler_base_v1
import a10_neutron_lbaas.contrail.v1.v1_context as a10

LOG = logging.getLogger(__name__)


class VipHandler(handler_base_v1.HandlerBaseV1):

    def create(self, vip):
        with a10.A10WriteStatusContext(self, vip) as c:
            status = c.client.slb.UP
            if not vip['admin_state_up']:
                status = c.client.slb.DOWN

            pool_name = self._pool_name(vip['pool_id'])

            p = PersistHandler(c, vip, self._meta_name(vip))
            p.create()

            templates = self.meta(vip, "template", {})

            if 'client_ssl' in templates:
                args = {'client_ssl_template': templates['client_ssl']}
                try:
                    c.client.slb.template.client_ssl.create(
                        '', '', '',
                        axapi_args=args)
                except acos_errors.Exists:
                    pass

            if 'server_ssl' in templates:
                args = {'server_ssl_template': templates['server_ssl']}
                try:
                    c.client.slb.template.server_ssl.create(
                        '', '', '',
                        axapi_args=args)
                except acos_errors.Exists:
                    pass

            vport_list = [{}]
            try:
                vip_args = {
                    'virtual_server': self.meta(vip, 'virtual_server', {})
                }
                vport_list = vip_args['virtual_server'].pop('vport_list', [{}])
                c.client.slb.virtual_server.create(
                    self._meta_name(vip),
                    vip['address'],
                    status,
                    axapi_args=vip_args)
            except acos_errors.Exists:
                pass

            LOG.debug("VPORT_LIST = %s", vport_list)
            try:
                if vport_list[0]:
                    vport_args = {'port': vport_list[0]}
                else:
                    vport_args = {'port': self.meta(vip, 'port', {})}
                c.client.slb.virtual_server.vport.create(
                    self._meta_name(vip),
                    self._meta_name(vip) + '_VPORT',
                    protocol=a10_os.vip_protocols(c, vip['protocol']),
                    port=vip['protocol_port'],
                    service_group_name=pool_name,
                    s_pers_name=p.s_persistence(),
                    c_pers_name=p.c_persistence(),
                    status=status,
                    axapi_args=vport_args)
            except acos_errors.Exists:
                pass

            i = 1
            for vport in vport_list[1:]:
                i += 1
                try:
                    vport_args = {'port': vport}
                    c.client.slb.virtual_server.vport.create(
                        self._meta_name(vip),
                        self._meta_name(vip) + '_VPORT' + str(i),
                        protocol=a10_os.vip_protocols(c, vip['protocol']),
                        port=vip['protocol_port'],
                        service_group_name=pool_name,
                        s_pers_name=p.s_persistence(),
                        c_pers_name=p.c_persistence(),
                        status=status,
                        axapi_args=vport_args)
                except acos_errors.Exists:
                    pass

            self.hooks.after_vip_create(c,  vip)

    def update(self, old_vip, vip):
        with a10.A10WriteStatusContext(self, vip) as c:
            status = c.client.slb.UP
            if not vip['admin_state_up']:
                status = c.client.slb.DOWN

            pool_name = self._pool_name( vip['pool_id'])

            p = PersistHandler(c,  vip, self._meta_name(vip))
            p.create()

            templates = self.meta(vip, "template", {})

            if 'client_ssl' in templates:
                args = {'client_ssl_template': templates['client_ssl']}
                c.client.slb.template.client_ssl.update(
                    '', '', '',
                    axapi_args=args)

            if 'server_ssl' in templates:
                args = {'server_ssl_template': templates['server_ssl']}
                c.client.slb.template.server_ssl.update(
                    '', '', '',
                    axapi_args=args)

            vport_args = {'port': self.meta(vip, 'port', {})}
            c.client.slb.virtual_server.vport.update(
                self._meta_name(vip),
                self._meta_name(vip) + '_VPORT',
                protocol=a10_os.vip_protocols(c, vip['protocol']),
                port=vip['protocol_port'],
                service_group_name=pool_name,
                s_pers_name=p.s_persistence(),
                c_pers_name=p.c_persistence(),
                status=status,
                axapi_args=vport_args)

            self.hooks.after_vip_update(c,  vip)

    def _delete(self, c,  vip):
        c.client.slb.virtual_server.delete(self._meta_name(vip))
        PersistHandler(c, vip, self._meta_name(vip)).delete()

    def delete(self, vip):
        with a10.A10DeleteContext(self, vip) as c:
            self._delete(c, vip)
            self.hooks.after_vip_delete(c, vip)


class PersistHandler(object):

    def __init__(self, c, vip, vip_name):
        self.c = c
        self.vip = vip
        self.c_pers = None
        self.s_pers = None
        self.name = vip_name

        if vip.get('session_persistence', None) is not None:
            self.sp = vip['session_persistence']
            if self.sp['type'] == 'HTTP_COOKIE':
                self.c_pers = self.name
            elif self.sp['type'] == 'SOURCE_IP':
                self.s_pers = self.name
            else:
                raise a10_ex.UnsupportedFeature()
        else:
            self.sp = None

    def c_persistence(self):
        return self.c_pers

    def s_persistence(self):
        return self.s_pers

    def create(self):
        if self.sp is None:
            return

        methods = {
            'HTTP_COOKIE':
                self.c.client.slb.template.cookie_persistence.create,
            'SOURCE_IP':
                self.c.client.slb.template.src_ip_persistence.create,
        }
        if self.sp['type'] in methods:
            try:
                methods[self.sp['type']](self.name)
            except acos_errors.Exists:
                pass

    def delete(self):
        if self.sp is None:
            return

        methods = {
            'HTTP_COOKIE':
                self.c.client.slb.template.cookie_persistence.delete,
            'SOURCE_IP':
                self.c.client.slb.template.src_ip_persistence.delete,
        }
        if self.sp['type'] in methods:
            try:
                methods[self.sp['type']](self.name)
            except Exception:
                pass
