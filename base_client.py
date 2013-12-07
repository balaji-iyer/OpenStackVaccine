import logging
import sys

class BaseClient:
    """ Abstract base class for clients.
        Defines interface that client may provide.
        Control class calls on these interfaces to create menace.
    """
    def __init__(self, name, conf, auth_info):
        try:
            self.menaces = conf["menaces"]
        except AttributeError:
            # Atleast some menace should be present.
            logging.error("Menaces not present in conf file. Check clients.json")
            sys.exit(-1)

        # its ok to not have any processes 
        # if we donot have process dependent menace
        self.processes = conf.get("processes", None)

        self.auth_info = auth_info
        
        self.process2inst = {}
        self.id2inst = {}
        self.id2vols = {}
        self.name = name


    def kill_instance(self, instaceId):
        raise NotImplementedError

    def kill_volume(self, instanceId, volume_id):
        raise NotImplementedError

    def list_instances(self):
        raise NotImplementedError

    def list_volumes(self, instance):
        raise NotImplementedError

    def kill_process(self, instanceId, processId):
        raise NotImplementedError

    def fail_DNS(self):
        raise NotImplementedError

    def flood_network(self):
        raise NotImplementedError

    def crashCPU(self, instanceId):
        raise NotImplementedError

    def crashIO(self, instanceId):
        raise NotImplementedError

    def detachVolume(self, instanceId):
        raise NotImplementedError

    def get_instance(self, instanceId):
        raise NotImplementedError

    def get_volume(self, instanceId, volume_id):
       raise NotImplementedError

    def get_registered_processes(self):
        return self.processes

    def get_registered_menaces(self):
        return self.menaces
