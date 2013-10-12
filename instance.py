"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
import util
from novaclient import client

class Instance:
    def __init__(self):
        pass

    def get_client(self):
        username = os.getenv('OS_USERNAME')
        tenant_name = os.getenv('OS_TENANT_NAME')
        password = os.getenv('OS_PASSWORD')
        auth_url = os.getenv('OS_AUTH_URL')

        return client.Client(username=username,
                                api_key=password,
                                project_id=tenant_name,
                                auth_url=auth_url)

if __name__ == "__main__":
    ins = Instance()
    client = ins.get_client()
    client.flavors.list()
