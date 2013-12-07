"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
import novaclient.v1_1
import cinderclient.v1
import time
from optparse import OptionParser

class Instance:
    client = None
    def __init__(self):
        username = os.getenv('OS_USERNAME')
        tenant_name = os.getenv('OS_TENANT_NAME')
        password = os.getenv('OS_PASSWORD')
        auth_url = os.getenv('OS_AUTH_URL')

        self.novaclient =  novaclient.v1_1.client.Client(username, password, tenant_name, auth_url, insecure=True, service_type="compute")
        self.cinderclient =  cinderclient.v1.client.Client(username, password, tenant_name, auth_url, insecure=True, service_type="volume")


    def get_flavor_list(self):
        for flavor in self.novaclient.flavors.list():
            print flavor

    def get_image_list(self):
        for image in self.novaclient.images.list():
            print image

    def boot_instance(self, count):
        instances = []
        for i in xrange(count):
            instance = None
            floating_ip = None
            volume = None
            instance_found = False
            for server in self.novaclient.servers.list():
                if "my-server-%s" % i in server.name:
                    instance_found = True
                    instance = server
                    break;
            if not instance_found:
                flavor = self.novaclient.flavors.find(ram=512);
                if flavor == None:
                    raise Exception
                imL = [x for x in self.novaclient.images.list() if x.name.find("ubuntu") > -1]
                if len(imL) > 0:
                    instance = self.novaclient.servers.create("my-server-%s" %i, imL[0], flavor=flavor)

                status = instance.status
                #Poll at 5 second interval, until status is no longer build
                while status == 'BUILD':
                    time.sleep(5)
                    instance = self.novaclient.servers.get(instance.id)
                    status = instance.status
            if not instance:
                raise Exception
            floating_ip = self.attach_floating_ips(instance)
            volume = self.attach_volume(instance, 2, "my-vol", "/dev/vdb")
            instances.append({
                "id": instance.id,
                "floating_ip": floating_ip,
                "volume": volume.id
            })
        return instances

    def attach_floating_ips(self, instance):
        floating_ip_list = self.novaclient.floating_ips.list()
        for floating_ip in floating_ip_list:
            if floating_ip.instance_id == instance.id:
                return floating_ip
        floating_ip = self.novaclient.floating_ips.create()
        if instance != None:
            instance.add_floating_ip(floating_ip)
        return floating_ip

    def attach_volume(self, instance, size, disp_name, device_name, discription=None):
        assert instance != None
        assert size != None and size > 0
        assert disp_name != None

        attached_volumes = self.novaclient.volumes.get_server_volumes(instance.id)
        if len(attached_volumes) > 0:
            for volume in attached_volumes:
                if volume.device == device_name:
                    return volume
        volume = self.cinderclient.volumes.create(size, display_name = disp_name)

        assert volume != None, "Failed to get volume"
        assert volume.display_name == disp_name

        vol = self.novaclient.volumes.create_server_volume(
                server_id=instance.id,
                volume_id=volume.id,
                device=device_name)

        assert vol.device == device_name
        assert vol.id == volume.id

        return volume


if __name__ == "__main__":
    import pdb;pdb.set_trace()
    os_client = Instance()
    os_client.get_flavor_list()
    os_client.get_image_list()
    instances = os_client.boot_instance(1)

