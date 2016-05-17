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


import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from a10_neutron_lbaas import a10_exceptions as ex

A10_CFG = None
Base = sqlalchemy.ext.declarative.declarative_base()

def get_base():
    return Base


def get_engine(url=None):
    if url is None:
        if A10_CFG is None:
            from a10_neutron_lbaas import a10_config
            A10_CFG = a10_config.A10Config()

        if not A10_CFG.get('use_database'):
            raise ex.InternalError("attempted to use database when it is disabled")
        url = A10_CFG.get('database_connection')

    return sqlalchemy.create_engine(url)


def get_session(url=None):
    DBSession = sqlalchemy.orm.sessionmaker(bind=get_engine())
    return DBSession()
