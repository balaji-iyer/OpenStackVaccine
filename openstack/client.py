from novaclient.v1_1 import client
from novaclient.exceptions import NotFound
from base_client import BaseClient
from instance import Instance
from volume import Volume
from menace import Menace
import logging
import re

class Client(BaseClient):
    def __init__(self, name, conf, os_auth_info):
        BaseClient.__init__(self, name, conf, os_auth_info)
        self.handle = client.Client(
                           os_auth_info["username"],
                           os_auth_info["password"],
                           os_auth_info["tenant_name"],
                           os_auth_info["auth_url"],
                           insecure=True,
                           service_type="compute")

        # Maybe the client doesn't prefer ssh route
        self.ssh_info = conf.get("ssh", None)

        servers = []
        try:
            servers.extend(self.handle.servers.list())
        except NotFound:
            logging.warn("No servers present for client %s" % name)

        self.pattern = re.compile("^" + os_auth_info["username"] + "-[0-9]{3}")
        for inst in servers:
            if not self.pattern.match(inst.name):
                continue
            instance = Instance(self, inst, self.ssh_info)
            instanceId = instance.get_id()

            self.id2inst[instanceId] = instance

            vols = []
            try:
                vols.extend(self.handle.volumes.get_server_volumes(instanceId))
            except NotFound:
                logging.warn("No volume attached for instance %s(%s)" % (instance.get_name(), instance.get_id()))

            volumes = self.id2vols[instanceId] = []
            for vol in vols:
                volumes.append(Volume(instance, vol))



    def is_owned_instance(self, instance):
        return instance.get_id() in self.id2inst

    def is_owned_volume(self, instance, volumeId):
        for volume in self.id2vols[instance.get_id()]:
            if volume.get_id() == volumeId:
                return True
        return False


    def list_instances(self):
        insts = self.handle.servers.list()

        # Update instance list in self.id2inst
        self.id2inst.clear()
        instances = []
        for inst in insts:
            if not self.pattern.match(inst.name):
                continue

            instance = Instance(self, inst, self.ssh_info)
            self.id2inst[instance.get_id()] = instance
            instances.append(instance)
        return  instances

    def list_volumes(self, instance):
        return self.get_attached_volumes(instance.get_id(), latest=True)

    def get_instance(self, instanceId, latest=False):
        assert instanceId != None
        instance = self.handle.servers.get(instanceId) if latest else self.id2inst.get(instanceId, None)
        if instance == None:
            raise Exception

        return instance

    def get_volume(self, instanceId, volume_id, latest=False):
        instance_obj = self.id2inst.get(instanceId, None)
        if instance_obj == None:
            raise Exception

        volumes = self.get_attached_volumes(instanceId, latest)

        for volume in volumes:
            if volume.get_id() == volume_id:
                return volume
        return None

    def get_attached_volumes(self, instanceId, latest=False):
        instance = self.id2inst.get(instanceId, None)
        if instance == None:
            raise Exception

        if latest:
            self.id2vols.clear()
            volumes = self.handle.volumes.get_server_volumes(instanceId)
            vols = []
            for volume in volumes:
                vols.append(Volume(instance, volume))
            self.id2vols[instanceId] = vols

        return self.id2vols[instanceId]

    def kill_volume(self, volume):
        volume_id = volume.get_id()
        instanceId = volume.get_instance_id()
        volume = self.get_volume(instanceId, volume_id)
        assert volume != None
        try:
            self.handle.volumes.delete_server_volume(instanceId, volume_id)
        except NotFound:
            logging.warn("Volume %s not found on instance %s" % (instanceId, volume_id))

    def _reattach_volume(self, volume):
        vol = self.handle.volumes.create_server_volume(
                server_id=volume.get_instance_id(),
                volume_id=volume.get_id(),
                device=volume.get_device())

    def can_apply_menace(self, menace):
        return menace in self.menaces

