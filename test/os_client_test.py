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
        assert instance.status == "SHUTOFF"
        print "Instance successfully shutoff"

        self.client._start_instance(instanceId)
        time.sleep(5)
        instance = self.client.get_instance(instanceId)
        assert instance.status == "ACTIVE"
        print "Instance successfully restarted"

    def test_kill_volume(self, instanceId, volume_id):
        instance = self.client.get_instance(instanceId)
        assert instance != None
        volume = self.client.get_volume(instanceId, volume_id)
        self.client.kill_volume(instanceId, volume_id)

        time.sleep(5)
        assert self.client.get_volume(instanceId, volume_id) == None
        print "Volume successfully detached"

        self.client._reattach_volume(volume)
        assert self.client.get_volume(instanceId, volume_id) == volume
        print "Volume successfully reattached"

if __name__ == "__main__":
        client = Instance()
        inst_info = client.boot_instance(1);

        test_client = TestOSClient(inst_info,
                                ["kill_instance"],
                                [],
                                1,
                                1,
                                {
                                    "username": os.getenv('OS_USERNAME'),
                                    "tenant_name": os.getenv('OS_TENANT_NAME'),
                                    "password": os.getenv('OS_PASSWORD'),
                                    "auth_url": os.getenv('OS_AUTH_URL')
                               })
        test_client.test_kill_instance(inst_info[0]["id"])
        import pdb;pdb.set_trace()
        test_client.test_kill_volume(inst_info[0]["id"], inst_info[0]["volume"])
