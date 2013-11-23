from novaclient.v1_1 import client
from base_client import BaseClient
from menace import Menace
import logging
class Client(BaseClient):
    def __init__(self, menaces, processes, os_auth_info):
        BaseClient.__init__(self, menaces, processes)
        self.handle = client.Client(os_auth_info["username"],
                                       os_auth_info["password"],
                                       os_auth_info["tenant_name"],
                                       os_auth_info["auth_url"],
                                       insecure=True,
                                       service_type="compute")

        for inst in self.handle.servers.list():
            self.id2inst[inst.id] = inst

    def is_owned_instance(self, instance):
        return instance.id in self.id2inst

    def is_owned_volume(self):
        return True

    def kill_volume(self, instanceId, volume_id):
        volume = self.get_volume(instanceId, volume_id)
        assert volume != None
        self.handle.volumes.delete_server_volume(instanceId, volume.id)

    def list_instances(self):
        instances = self.handle.servers.list()

        # Update instance list in self.id2inst
        self.id2inst.clear()
        for instance in instances:
            self.id2inst[instance.id] = instance
        return instances

    def list_volumes(self, instanceId):
        pass

    def kill_process(self):
        pass

    def get_instance(self, instanceId, latest=False):
        assert instanceId != None
        instance = self.handle.servers.get(instanceId) if latest else self.id2inst.get(instanceId, None)
        if instance == None:
            raise Exception

        return instance

    def start_instance(self, instance):
        if (instance != None and
                instance.status != "ACTIVE"):
            instance.start()

    def resume_instance(self, instance):
        if (instance != None and
                instance.status != "ACTIVE"):
            instance.resume()

    def stop_instance(self, server):
        if (server != None and
                server.status == "ACTIVE"):
            server.stop();

    def pause_instance(self, server):
        if (server != None and
            server.status == "ACTIVE"):
            server.pause();

    def get_volume(self, instanceId, volume_id):
        instance_obj = self.id2inst.get(instanceId, None)
        if instance_obj == None:
            raise Exception

        volumes = self.handle.volumes.get_server_volumes(instanceId)

        for volume in volumes:
            if volume.volumeId == volume_id:
                return volume
        return None

    def get_attached_volumes(self, instanceId):
        instance_obj = self.id2inst.get(instanceId, None)
        if instance_obj == None:
            raise Exception

        volumes = self.handle.volumes.get_server_volumes(instanceId)
        return volumes
    def _reattach_volume(self, volume):
        vol = self.handle.volumes.create_server_volume(
                server_id=volume.serverId,
                volume_id=volume.volumeId,
                device=volume.device)

    def can_apply_menace(self, menace):
        return menace in self.menaces

