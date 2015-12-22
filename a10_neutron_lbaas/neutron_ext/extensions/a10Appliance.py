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

import a10_neutron_lbaas.localization as localization
import a10_neutron_lbaas.neutron_ext.common.constants as constants

import abc

from neutron.api import extensions
from neutron.api.v2 import attributes
from neutron.api.v2 import resource_helper
from neutron.common import exceptions
from neutron.services import service_base

import six

# Neutron is finicky. Sometimes _ is defined, sometimes it isn't
localization.install()


def singular(plural):
    singulars = resource_helper.build_plural_mappings({}, {plural: {}})
    return singulars[plural]


A10_APPLIANCE_RESOURCES = 'a10_appliances'
A10_APPLIANCE_RESOURCE = singular(A10_APPLIANCE_RESOURCES)

RESOURCE_ATTRIBUTE_MAP = {
    A10_APPLIANCE_RESOURCES: {
        'id': {
            'allow_post': False,
            'allow_put': True,
            'validate': {
                'type:uuid': None
            },
            'is_visible': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'required_by_policy': True,
            'is_visible': True
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:string': None
            },
            'is_visible': True,
            'default': ''
        },
        'description': {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:string': None
            },
            'is_visible': True,
            'default': '',
        },
        'host': {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:string': None
            },
            'is_visible': True
        },
        'username': {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:string': None
            },
            'is_visible': True
        },
        'password': {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:string': None
            },
            'is_visible': False
        },
        'api_version': {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:string': None
            },
            'is_visible': True
        }
    }
}


class A10Appliance(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return "A10 Appliances"

    @classmethod
    def get_alias(cls):
        return constants.A10_APPLIANCE_EXT

    @classmethod
    def get_namespace(cls):
        return "http://docs.openstack.org/ext/neutron/a10_appliance/api/v1.0"

    @classmethod
    def get_updated(cls):
        return "2015-11-18T16:17:00-07:00"

    @classmethod
    def get_description(cls):
        return ("A10 Appliances")

    @classmethod
    def get_resources(cls):
        """Returns external resources."""
        my_plurals = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP)
        attributes.PLURALS.update(my_plurals)
        attr_map = RESOURCE_ATTRIBUTE_MAP
        resources = resource_helper.build_resource_info(my_plurals,
                                                        attr_map,
                                                        constants.A10_APPLIANCE)

        return resources

    def update_attributes_map(self, attributes):
        super(A10Appliance, self).update_attributes_map(
            attributes,
            extension_attrs_map=RESOURCE_ATTRIBUTE_MAP)

    def get_extended_resources(self, version):
        if version == "2.0":
            return RESOURCE_ATTRIBUTE_MAP
        else:
            return {}


class A10ApplianceNotFoundError(exceptions.NotFound):
    def __init__(self, a10_appliance_id):
        self.msg = _("A10 Appliance {} could not be found.")
        super(A10ApplianceNotFoundError, self).__init__()


class A10ApplianceInUseError(exceptions.InUse):
    def __init__(self, a10_appliance_id):
        self.message = _("A10 Appliance is in use and cannot be deleted.")
        self.msg = self.message
        super(A10ApplianceInUseError, self).__init__()


@six.add_metaclass(abc.ABCMeta)
class A10AppliancePluginBase(service_base.ServicePluginBase):

    def get_plugin_name(self):
        return constants.A10_APPLIANCE

    def get_plugin_description(self):
        return constants.A10_APPLIANCE

    def get_plugin_type(self):
        return constants.A10_APPLIANCE

    def __init__(self):
        super(A10AppliancePluginBase, self).__init__()

    @abc.abstractmethod
    def get_a10_appliances(self, context, filters=None, fields=None):
        pass

    @abc.abstractmethod
    def create_a10_appliance(self, context, appliance):
        pass

    @abc.abstractmethod
    def get_a10_appliance(self, context, id, fields=None):
        pass

    @abc.abstractmethod
    def update_a10_appliance(self, context, appliance):
        pass

    @abc.abstractmethod
    def delete_a10_appliance(self, context, id):
        pass
