from clients.os_client import OS_Client
from init.futuregrid_boot_os import Instance
import os
import time
class TestOSClient:
    def __init__(self, instances, menaces, processes, freq, freq_unit, os_auth_info):
        self.client = OS_Client(instances, menaces, processes, freq, freq_unit, os_auth_info)
        assert self.client != None


    def test_kill_instance(self, instanceId):
        instance = self.client.get_instance(instanceId)
        assert instance != None

        self.client.kill_instance(instanceId)
        time.sleep(5)

        instance = self.client.get_instance(instanceId)
        assert instance == None

if __name__ == "__main__":
        client = Instance()
        import pdb;pdb.set_trace()
        inst_info = client.boot_instance(1);

        test_client = TestOSClient(inst_info,
                                ["kill_instance"],
                                [],
                                1,
                                1,
                                {
                                    "username": os.getenv('OS_USERNAME'),
                                    "tenant_name": os.getenv('OS_TENENT_NAME'),
                                    "password": os.getenv('OS_PASSWORD'),
                                    "auth_url": os.getenv('OS_AUTH_URL')
                               })
        test_client.test_kill_instance(inst_info["id"])
