"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
from novaclient.v1_1 import client
from optparse import OptionParser

class Instance:
    client = None
    def __init__(self):
        username = os.getenv('OS_USERNAME')
        tenant_name = os.getenv('OS_TENANT_NAME')
        password = os.getenv('OS_PASSWORD')
        auth_url = os.getenv('OS_AUTH_URL')

        self.client =  client.Client(username, password, tenant_name, auth_url, insecure=True, service_type="compute")

    def get_flavor_list(self):
        for flavor in self.client.flavors.list():
            print flavor

    def get_image_list(self):
        for image in self.client.images.list():
            print image

if __name__ == "__main__":
	import pdb;pdb.set_trace();
	os_client = Instance();
	os_client.get_flavor_list();
	os_client.client.servers.list()
	os_client.get_image_list()
	fl = os_client.client.flavors.find(ram=512);
	imL = [x for x in os_client.client.images.list() if x.name.find("ubuntu") > -1]
	if len(imL) > 0:
		os_client.client.servers.create("my-server", imL[0], flavor=fl)
