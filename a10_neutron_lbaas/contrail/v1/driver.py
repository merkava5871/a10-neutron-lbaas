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

import svc_monitor.services.loadbalancer.drivers.abstract_driver as abstract_driver
import vnc_api.vnc_api import *
from svc_monitor import db

class ThunderContrailDriver(abstract_driver.ContrailLoadBalancerAbstractDriver):
    def __init__(self, name, manager, api, db, args=None):
        self._name = name
        self._api = api
        self._svc_mon = manager
        self._args = args
        self.db = db

    def create_vip(self, vip):
        raise Exception("Not implemented")

    def update_vip(self, old_vip, vip):
        raise Exception("Not implemented")

    def delete_vip(self, vip):
        raise Exception("Not implemented")

    def create_pool(self, pool):
        raise Exception("Not implemented")

    def update_pool(self, old_pool, pool):
        raise Exception("Not implemented")

    def delete_pool(self, pool):
        old_pool_svc, new_pool_svc = self.locate_resources(pool['id'], False)
        if old_pool_svc:
            self.delete_service(old_pool_svc)
            self.db.pool_remove(pool['id'])

    def stats(self, pool_id):
        raise Exception("Not implemented")

    def create_member(self, member):
        raise Exception("Not implemented")

    def update_member(self, old_member, member):
        raise Exception("Not implemented")

    def delete_member(self, member):
        raise Exception("Not implemented")
    
    def create_pool_health_monitor(self, 
                                   health_monitor,
                                   pool_id):
        raise Exception("Not implemented")
    
    def delete_pool_health_monitor(self, health_monitor, pool_id):
        raise Exception("Not implemented")
    
    def update_health_monitor(self, 
                              old_health_monitor,
                              health_monitor,
                              pool_id):
        raise Exception("Not implemented")
