# Copyright (C) 2016 A10 Networks Inc. All rights reserved.
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

from __future__ import absolute_import

import logging
from openstack_dashboard.api.neutron import NeutronAPIDictWrapper
from openstack_dashboard.api.neutron import neutronclient

from a10_neutron_lbaas_client.resources import a10_scaling_group

LOG = logging.getLogger(__name__)


class A10ScalingGroup(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingGroup, self).__init__(apiresource)


class A10ScalingGroupMember(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingGroupMember, self).__init__(apiresource)


class A10ScalingGroupWorker(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingGroupWorker, self).__init__(apiresource)


class A10ScalingGroupWorker(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingGroupWorker, self).__init__(apiresource)


class A10ScalingPolicy(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingPolicy, self).__init__(apiresource)


class A10ScalingPolicyReaction(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingPolicyReaction, self).__init__(apiresource)


class A10ScalingAction(NeutronAPIDictWrapper):
    """Wrapper for a10_scaling_group dictionary"""
    def __init__(self, apiresource):
        super(A10ScalingAction, self).__init__(apiresource)


# Scaling Groups

def get_a10_scaling_groups(request, **kwargs):
    rv = neutronclient(request).list_a10_scaling_groups(**kwargs).get(a10_scaling_group.RESOURCES)
    return map(A10ScalingGroup, rv)


def get_a10_scaling_group(request, id, **params):
    rv = neutronclient(request).show_a10_scaling_group(id).get(a10_scaling_group.RESOURCE)
    return A10ScalingGroup(rv)


def delete_a10_scaling_group(request, id):
    neutronclient(request).delete_a10_scaling_group(id)


def create_a10_scaling_group(request, **kwargs):
    body = {a10_scaling_group.RESOURCE: kwargs}
    rv = neutronclient(request).create_a10_scaling_group(body=body).get(a10_scaling_group.RESOURCE)
    return A10ScalingGroup(rv)


def update_a10_scaling_group(request, id, **kwargs):
    body = {a10_scaling_group.RESOURCE: kwargs}
    rv = neutronclient(request).update_a10_scaling_group(id, body=body).get(a10_scaling_group.RESOURCE)
    return A10ScalingGroup(rv)

# Scaling Policy

def get_a10_scaling_policies(request, **kwargs):
    rv = neutronclient(request).list_a10_scaling_policies(**kwargs).get(a10_scaling_policy.RESOURCES)
    return map(A10ScalingPolicy, rv)


def get_a10_scaling_policy(request, id, **params):
    rv = neutronclient(request).show_a10_scaling_policy(id).get(a10_scaling_policy.RESOURCE)
    return A10ScalingPolicy(rv)


def delete_a10_scaling_policy(request, id):
    neutronclient(request).delete_a10_scaling_policy(id)


def create_a10_scaling_policy(request, **kwargs):
    body = {a10_scaling_policy.RESOURCE: kwargs}
    rv = neutronclient(request).create_a10_scaling_policy(body=body).get(a10_scaling_policy.RESOURCE)
    return A10ScalingPolicy(rv)


def update_a10_scaling_policy(request, id, **kwargs):
    body = {a10_scaling_policy.RESOURCE: kwargs}
    rv = neutronclient(request).update_a10_scaling_policy(id, body=body).get(a10_scaling_policy.RESOURCE)
    return A10ScalingPolicy(rv)

# Scaling Policy Reactions

def get_a10_scaling_policy_reactions(request, **kwargs):
    rv = neutronclient(request).list_a10_scaling_policies(**kwargs).get(a10_scaling_policy_reaction.RESOURCES)
    return map(A10ScalingPolicyReaction, rv)


def get_a10_scaling_policy_reaction(request, id, **params):
    rv = neutronclient(request).show_a10_scaling_policy_reaction(id).get(a10_scaling_policy_reaction.RESOURCE)
    return A10ScalingPolicyReaction(rv)


def delete_a10_scaling_policy_reaction(request, id):
    neutronclient(request).delete_a10_scaling_policy_reaction(id)


def create_a10_scaling_policy_reaction(request, **kwargs):
    body = {a10_scaling_policy_reaction.RESOURCE: kwargs}
    rv = neutronclient(request).create_a10_scaling_policy_reaction(body=body).get(a10_scaling_policy_reaction.RESOURCE)
    return A10ScalingPolicyReaction(rv)


def update_a10_scaling_policy_reaction(request, id, **kwargs):
    body = {a10_scaling_policy_reaction.RESOURCE: kwargs}
    rv = neutronclient(request).update_a10_scaling_policy_reaction(id, body=body).get(a10_scaling_policy_reaction.RESOURCE)
    return A10ScalingPolicyReaction(rv)


# Scaling Alarms

def get_a10_scaling_alarms(request, **kwargs):
    rv = neutronclient(request).list_a10_scaling_policies(**kwargs).get(a10_scaling_alarm.RESOURCES)
    return map(A10ScalingAlarm, rv)


def get_a10_scaling_alarm(request, id, **kwargs):
    rv = neutronclient(request).show_a10_scaling_alarm(id).get(a10_scaling_alarm.RESOURCE)
    return A10ScalingAlarm(rv)


def delete_a10_scaling_alarm(request, id):
    neutronclient(request).delete_a10_scaling_alarm(id)


def create_a10_scaling_alarm(request, **kwargs):
    body = {a10_scaling_alarm.RESOURCE: kwargs}
    rv = neutronclient(request).create_a10_scaling_alarm(body=body).get(a10_scaling_alarm.RESOURCE)
    return A10ScalingAlarm(rv)


def update_a10_scaling_alarm(request, id, **kwargs):
    body = {a10_scaling_alarm.RESOURCE: kwargs}
    rv = neutronclient(request).update_a10_scaling_alarm(id, body=body).get(a10_scaling_alarm.RESOURCE)
    return A10ScalingAlarm(rv)


# Scaling Actions

def get_a10_scaling_actions(request, **kwargs):
    rv = neutronclient(request).list_a10_scaling_policies(**kwargs).get(a10_scaling_action.RESOURCES)
    return map(A10ScalingAction, rv)


def get_a10_scaling_action(request, id, **kwargs):
    rv = neutronclient(request).show_a10_scaling_action(id).get(a10_scaling_action.RESOURCE)
    return A10ScalingAction(rv)


def delete_a10_scaling_action(request, id):
    neutronclient(request).delete_a10_scaling_action(id)


def create_a10_scaling_action(request, **kwargs):
    body = {a10_scaling_action.RESOURCE: kwargs}
    rv = neutronclient(request).create_a10_scaling_action(body=body).get(a10_scaling_action.RESOURCE)
    return A10ScalingAction(rv)


def update_a10_scaling_action(request, id, **kwargs):
    body = {a10_scaling_action.RESOURCE: kwargs}
    rv = neutronclient(request).update_a10_scaling_action(id, body=body).get(a10_scaling_action.RESOURCE)
    return A10ScalingAction(rv)
