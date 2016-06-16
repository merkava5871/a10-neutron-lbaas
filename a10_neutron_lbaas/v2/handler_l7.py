# Copyright 2016, A10 Networks
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

import acos_client.errors as acos_errors

from a10_neutron_lbaas.acos import openstack_mappings
from a10_neutron_lbaas import constants

import handler_base_v2
import handler_persist
import v2_context as a10


LOG = logging.getLogger(__name__)
#  "name": name,
#  "redirect-rewrite": site_switching,
#  "host-switching": host_switching,
#  "site-switching": site_switching,

# def create(self, name, redirect_rewrite=[], host_switching=[],
#            site_switching=[], *args, **kwargs):
#     if self.exists(name):
#         raise acos_errors.Exists

#     return self._set(name, redirect_rewrite, host_switching, site_switching, args, kwargs)


class L7PolicyHandler(handler_base_v2.HandlerBaseV2):
    def __init__(self, a10_driver, openstack_manager, neutron=None):
        super(L7PolicyHandler, self).__init__(a10_driver, openstack_manager, neutron)

    def _set(self, set_method, c, context, policy):
        set_method(**_transform(policy))

    def _create(self, c, context, policy):
        self._set(c.client.slb.template.http_template.create, c, context, policy)

    def _validate(self, policy):
        # Check to make sure they're not using Reject - we don't support that yet.
        # 400 Bad Request is the recommended rejection code, we only have 3xx at our disposal
        # TODO(mdurrant) Get these from string constants in neutron_lbaas
        if str.upper(str(policy.action)) == "REJECT":
            raise L7PolicyActionNotImplementedError("REJECT is not implemented")

    def _transform(self, policy):
        """
        Transform actions into the corresponding HTTP Template member.
        """
        rv = {}

        # Redirect to service group.  Get the pool ID.
        action = str.upper(policy.action)
        if action == "REDIRECT_TO_POOL":
            pool_id = policy.pool_id
        elif action == "REDIRECT_TO_URL":
            redirect_url= policy.redirect_url
        name = policy.id

        try:
            _validate(policy)
        except ValidationError as vex:
            LOG.exception(vex)

        return {"http": rv}

    def create(self, context, policy):
        """
        For creates, we don't do anything.  This information is merely stored to be used when writing aflex rules down the line.
        """
        try:
            policy = self._transform(policy)
            with a10.A10WriteStatusContext(self, context, policy) as c:
                self._create(c, context, policy)
        except ValidationError as vex:
            LOG.exception(vex.message)
        except Exception as ex:
            LOG.exception(ex)

    def update(self, context, old_policy, policy):
        """
        For updates, we have to iterate through every vport this thing is bound to, every aflex script it's bound to (that's exists as an l7 policy), and update URL/pool redirects and rejects accordingly.  Merely substitutes the action taken by AfleX for the list of conditions it receives.
        """
        # with a10.A10WriteStatusContext(self, context, policy) as c:
        #     self._update(c, context, policy)
        pass

    def delete(self, context, policy):
        """
        Delete = no longer bound to vport.  The rules still exist, they're just not attached to the port anymore.  When the last rule in a policy is deleted, the policy will also get deleted.
        """


class L7RuleHandler(handler_base_v2.HandlerBaseV2):
    def __init__(self, a10_driver, openstack_manager, neutron=None):
        super(L7RuleHandler, self).__init__(a10_driver, openstack_manager, neutron)

    def _set(self, set_method, c, context, rule):
        raise NotImplementedError("Not implemented.")

    def create(self, context, rule):
        pass
        # with a10.A10WriteStatusContext(self, context, rule) as c:
        #     self._create(c, context, rule)

    def update(self, context, old_rule, rule):
        pass
        # with a10.A10WriteStatusContext(self, context, rule) as c:
        #     self._update(c, context, rule)

    def delete(self, context, rule):
        pass
        # with a10.A10DeleteContext(self, context, rule) as c:
        #     self._delete(c, context, rule)
