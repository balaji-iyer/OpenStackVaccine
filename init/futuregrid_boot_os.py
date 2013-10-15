"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
import util
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
        for flavor in self.client.flavor.list():
            print flavor

if __name__ == "__main__":
    parser = OptionParser()
    nt = Instance()
