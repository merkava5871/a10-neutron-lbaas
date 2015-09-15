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
# flake8: noqa

from a10_openstack_lb_v1 import A10OpenstackLBV1
try:
    from a10_openstack_lb_v2 import A10OpenstackLBV2
except ImportError:
    pass

try:
   from a10_contrail_v1 import A10ContrailDriverV1 
except ImportError:
    pass

from version import VERSION
