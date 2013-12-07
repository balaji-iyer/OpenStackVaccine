""" Script accomplishes the following tasks.
    1. Init Servers
    2. Give a floating ip
    3. Attach a volume at /dev/vdb
"""
from OSV import CLIENTS_FILE
from openstack.instance import Instance
from optparse import OptionParser
import os
import cinderclient.v1
import json
import logging
import novaclient.v1_1
import paramiko
import time
import sys

class OS_Instance:
    client = None
    def __init__(self):
        username = os.getenv('OS_USERNAME')
        tenant_name = os.getenv('OS_TENANT_NAME')
        password = os.getenv('OS_PASSWORD')
        auth_url = os.getenv('OS_AUTH_URL')
        self.username = username

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
        for i in range(1, count + 1):
            instance = None
            floating_ip = None
            volume = None
            instance_found = False
            for server in self.novaclient.servers.list():
                if "%s-%03d" % (self.username, i) == server.name:
                    instance_found = True
                    instance = server
                    break;
            if not instance_found:
                flavor = self.novaclient.flavors.find(ram=512);
                if flavor == None:
                    raise Exception
                imL = [x for x in self.novaclient.images.list() if x.name.find("ubuntu") > -1]
                if len(imL) > 0:
                    instance = self.novaclient.servers.create("%s-%03d" %(self.username, i), imL[0], flavor=flavor)

                status = instance.status
                #Poll at 5 second interval, until status is no longer build
                while status == 'BUILD':
                    time.sleep(5)
                    instance = self.novaclient.servers.get(instance.id)
                    status = instance.status
            if not instance:
                raise Exception
            logging.info("Booting Instance %s" % instance)
            instances.append(instance)
        return instances

    def attach_floating_ips(self, instance):

        assert instance != None
        floating_ip_list = self.novaclient.floating_ips.list()

        # Return floating ip if instance is up and
        # already has an IP attached.

        for floating_ip in floating_ip_list:
            if floating_ip.instance_id == instance.id:
                logging.info("Instance %s: Attaching Floating Ip %s" % (instance, floating_ip))
                return floating_ip

        # Else return any vacant floating ip
        # No point creating a new one.
        floating_ip = False
        for f_ip in floating_ip_list:
            if f_ip.instance_id == None:
                floating_ip = f_ip
                break

        # If no available floating IP. Create One
        if not floating_ip:
            floating_ip = self.novaclient.floating_ips.create()

        instance.add_floating_ip(floating_ip)
        time.sleep(5)
        logging.info("Instance %s: Attaching Floating Ip %s" % (instance, floating_ip))
        return floating_ip

    def attach_volume(self, instance, size, disp_name, device_name, discription=None):
        assert instance != None
        assert size != None and size > 0
        assert disp_name != None

        volumes = self.novaclient.volumes.get_server_volumes(instance.id)
        if len(volumes) > 0:
            for volume in volumes:
                if volume.device == device_name:
                    return volume

        volume = None
        volumes = self.cinderclient.volumes.list()
        for vol in volumes:
            if len(vol.attachments) == 0:
                volume = vol
                break

        # Else create a volume.
        if not volume:
            volume = self.cinderclient.volumes.create(size, display_name = disp_name)
            logging.info("Instance %s: Creating Volume %s" % (instance, volume))
            status = volume.status
            #Poll at 5 second interval, until status is no longer build
            while status != 'available':
                logging.info("Instance %s: Waiting 5 sec for Volume %s" % (instance, volume))
                time.sleep(5)
                instance = self.cinderclient.volumes.get(volume.id)
                status = volume.status

        assert volume != None, "Failed to get volume"

        vol = self.novaclient.volumes.create_server_volume(
                server_id=instance.id,
                volume_id=volume.id,
                device=device_name)

        assert vol.device == device_name
        assert vol.id == volume.id
        logging.info("Instance %s: Attaching Volume %s" % (instance, volume))
        return volume


if __name__ == "__main__":
    parser = OptionParser()
    logging.basicConfig(level=logging.INFO)
    parser.add_option("-c", "--count", dest="count", type="int", default=1)
    (options, args) = parser.parse_args()

    import pdb;pdb.set_trace()
    os_client = OS_Instance()
    instances = []

    os_instances = os_client.boot_instance(options.count)
    conf_file = open(os.path.abspath(CLIENTS_FILE))
    clients_json = json.load(conf_file)

    conf = None
    for client_json in clients_json:
        if "openstack" == client_json["name"]:
            conf = client_json

    assert "client" in client_json
    assert "ssh" in client_json["client"]

    ssh_info = client_json["client"]["ssh"]
    i = 0;
    for os_instance in os_instances:
        floating_ip = os_client.attach_floating_ips(os_instance)
        volume = os_client.attach_volume(os_instance, 2, "my-vol-%s" % i, "/dev/vdb")

        instance = Instance(os_instance, ssh_info)
        i += 1;
        instance.exec_script("inf_py")

