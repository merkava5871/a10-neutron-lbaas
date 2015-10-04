# Copyright 2014, Doug Wiegl ey (dougwig), A10 Networks
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

import a10_neutron_lbaas.contrail.a10_context as a10_context


class A10Context(a10_context.A10Context):
    pass


class A10WriteContext(a10_context.A10WriteContext):
    pass


class A10WriteStatusContext(a10_context.A10WriteContext):

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
	   
            # replace with call to contrail back end
            # self.openstack_driver._active(
            #     self.openstack_context,
            #     self.handler._model_type(),
            #     self.openstack_lbaas_obj['id'])
            m = "Successfully created %s of type %".format(self.handler._model_type(),
                                                           self.openstack_lbaas_obj['id'])
           
	   
	    self.a10_driver.LOG.info(m)
        else:
	   # if 'id' in self.openstack_lbaas_obj:
           m = "Failed to create` %s of type %".format(self.handler._model_type(),
                                                            self.openstack_lbaas_obj['id'])
           self.a10_driver.LOG.warn(m)
	    #else:
		#pass
            # Replace with call to contrail back end
            # self.openstack_driver._failed(
            #     self.openstack_context,
            #     self.handler._model_type(),
            #     self.openstack_lbaas_obj['id'])

        super(A10WriteStatusContext, self).__exit__(exc_type, exc_value,
                                                    traceback)


class A10DeleteContext(a10_context.A10DeleteContextBase):

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            # self.openstack_driver._db_delete(
            #     self.openstack_context,
            #     self.handler._model_type(),
            #     self.openstack_lbaas_obj['id'])
	    print("START HERE")
	    print(self.openstack_lbaas_obj)
            import pdb
	    pdb.set_trace()
	    #if 'id' in self.openstack_lbaas_obj:
	    m = "Successfully deleted %s of type %".format(self.handler._model_type(),
                                                               self.openstack_lbaas_obj['id'])
  	    self.a10_driver.LOG.info(m)
	    
	    #else:
	        #pass

        super(A10DeleteContext, self).__exit__(exc_type, exc_value, traceback)

    def remaining_root_objects(self):
        # ctx = self.openstack_context
        # d = self.handler.openstack_driver
        # n = d._pool_total(ctx, self.tenant_id)
        return 1


class A10WriteHMStatusContext(a10_context.A10WriteContext):

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            # self.openstack_driver._hm_active(
            #     self.openstack_context,
            #     self.openstack_lbaas_obj['id'],
            #     self.openstack_lbaas_obj['pool_id'])
            m = "Successfully wrote  %s of type %".format(self.handler._model_type(),
                                                          self.openstack_lbaas_obj['id'])
            self.a10_driver.LOG.info(m)
        else:
            # self.openstack_driver._hm_failed(
            #     self.openstack_context,
            #     self.openstack_lbaas_obj['id'],
            #     self.openstack_lbaas_obj['pool_id'])
            m = "Failed to create` %s of type %".format(self.handler._model_type(),
                                                        self.openstack_lbaas_obj['id'])
            self.a10_driver.LOG.warn(m)

        super(A10WriteHMStatusContext, self).__exit__(exc_type, exc_value,
                                                      traceback)


class A10DeleteHMContext(a10_context.A10WriteContext):

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            # self.openstack_driver._hm_db_delete(
            #     self.openstack_context,
            #     self.openstack_lbaas_obj['id'],
            #     self.openstack_lbaas_obj['pool_id'])
            m = "Successfully de;eted %s of type %".format(self.handler._model_type(),
                                                           self.openstack_lbaas_obj['id'])
            self.a10_driver.LOG.omfp(m)
        super(A10DeleteHMContext, self).__exit__(exc_type, exc_value,
                                                 traceback)
