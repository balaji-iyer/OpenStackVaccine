class Client:
    """ Abstract base class for clients.
        Defines interface that client may provide.
        Control class calls on these interfaces to create menace.
    """
    def __init__(self, menaces, processes):
        self.menaces = menaces
        self.processes = processes
        self.process2inst = {}
        self.id2inst = {}


    def kill_instance(self, instaceId):
        raise NotImplementedError

    def kill_volume(self, instanceId, volume_id):
        raise NotImplementedError

    def list_instances(self):
        raise NotImplementedError

    def list_volumes(self, instanceId):
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

