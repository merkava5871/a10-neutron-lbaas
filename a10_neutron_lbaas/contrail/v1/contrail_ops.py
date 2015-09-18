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

from svc_monitor.config_db import *
from svc_monitor.config_db import HealthMonitorSM
from svc_monitor.config_db import LoadbalancerPoolSM
from svc_monitor.config_db import LoadbalancerMemberSM


class ContrailOpsV1(object):

    def __init__(self, driver):
        # We don't need to talk to Openstack directly anymore
        # We talk to VNC
        self._db = driver._db
        self._api = driver._api
        self._svc_mon = driver._svc_mon
        self.logger = self._svc_mon.logger

    def hm_binding_count(self, hm_id):
        result = 0
        try:
            lb_hm = self.hm_get(hm_id)
            result = len(lb_hm.loadbalancer_pools or ())
        except Exception as ex:
            self.logger.log_error("db entry missing for lb healthmonitor %s" %
                                  (hm_id))
        return result

    def hm_get(self, hm_id):
        lb_hm = None
        hm = object()
        try:
            lb_hm = HealthMonitorSM.locate(hm_id, hm)
        except Exception as ex:
            self.logger.log_error("db entry missing for lb healthmonitor %s" %
                                  (hm_id))
        return lb_hm

    def member_get_ip(self, member, use_float=False):
        raise Exception("Not implemented!")

    def member_count(self, member):
        raise Exception("Not implemented!")

    def member_get(self, member_id):
        return LoadbalancerMemberSM.get(member_id)

    def pool_get(self, pool_id):
        return LoadbalancerPoolSM.get(pool_id)

    def pool_get_tenant_id(self, pool_id):
        pool = self.pool_get(pool_id)
        return pool["tenant_id"]

    def vip_get(self, vip_id):
        raise Exception("Not implemented!")

    def vip_get_id(self, pool_id):
        raise Exception("Not implemented!")
