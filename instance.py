"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
import util
from novaclient.v1_1 import client

class Instance:
    def __init__(self):
        pass

    def get_client(self):
        username = os.getenv('OS_USERNAME')
        tenant_name = os.getenv('OS_TENANT_NAME')
        password = os.getenv('OS_PASSWORD')
        auth_url = os.getenv('OS_AUTH_URL')

        return client.Client(username, password, tenant_name, auth_url, insecure=True, service_type="compute")

if __name__ == "__main__":
    ins = Instance()
    nt = ins.get_client()
    print nt.flavors.list()
