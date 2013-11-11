"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
from novaclient.v1_1 import client
import time
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

    def boot_instance(self, count):
        instances = []
        for i in xrange(count):
            flavor = self.client.flavors.find(ram=512);
            instance = None
            if len(flavor) == 0:
                raise Exception
            imL = [x for x in self.client.images.list() if x.name.find("ubuntu") > -1]
            if len(imL) > 0:
                instance = self.client.servers.create("my-server-" + i, imL[0], flavor=flavor)

            status = instance.status
            #Poll at 5 second interval, until status is no longer build
            while status == 'BUILD':
                time.sleep(5)
                instance = self.client.servers.get(instance.id)
                status = instance.status

            floating_ip = self.attach_floating_ips(instance)
            volume = self.attach_volume(instance, 2, "my-vol-i", "/dev/vdb")
            instances.push({
                    "instance": instance.id,
                    "floating_ip": floating_ip,
                    "volume": volume.id

                })
        return instances

    def attach_floating_ips(self, instance):
        floating_ip = self.client.floating_ips.create()
        if instance != None:
            instance.add_floating_ip(floating_ip)
        return floating_ip

    def attach_volume(self, instance, size, disp_name, device_name, discription=None):
        assert instance != None
        assert size != None and size > 0
        assert disp_name != None

        attached_volumes = self.client.volumes.get_server_volumes(instance.id)
        if len(attached_volumes) > 0:
            for vol in attached_volumes:
                assert vol.device != device_name

        volume = self.client.volumes.create(
                    size=size,
                    display_name=disp_name,
                    display_description=discription)

        assert volume != None, "Failed to get volume"
        assert volume.name == disp_name

        vol = self.client.volumes.create_server_volume(
                server_id=instance.id,
                volume_id=volume.id,
                device=device_name)

        assert vol.device == device_name
        assert vol.id == volume.id

        return volume


if __name__ == "__main__":
    import pdb;pdb.set_trace();
    os_client = Instance()
    os_client.get_flavor_list()
    os_client.get_image_list()
    instances = os_client.boot_instance(1)

