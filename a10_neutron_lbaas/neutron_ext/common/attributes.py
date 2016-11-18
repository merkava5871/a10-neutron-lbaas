# Copyright 2016,  A10 Networks
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

try:
    import neutron.common.constants as old_constants
except ImportError:
    old_constants = None

try:
    import neutron.api.attributes as old_attributes
except ImportError:
    old_attributes = None

try:
    import neutron_lib.constants as lib_constants
except ImportError:
    lib_constants = None

try:
    import neutron_lib.api.converters as lib_converters
except ImportError:
    lib_converters = None


def _find(*args):
    for f in args:
        try:
            return f()
        except AttributeError:
            pass

convert_to_int = _find(lambda: old_attributes.convert_to_int,
                       lambda: lib_converters.convert_to_int)
convert_to_list = _find(lambda: old_attributes.convert_to_list,
                        lambda: lib_converters.convert_to_list)
convert_kvp_to_list = _find(lambda: old_attributes.convert_kvp_to_list,
                            lambda: lib_converters.convert_kvp_to_list)
ATTR_NOT_SPECIFIED = _find(lambda: old_constants.ATTR_NOT_SPECIFIED,
                           lambda: lib_constants.ATTR_NOT_SPECIFIED)
