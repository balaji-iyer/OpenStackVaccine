"""
    Abstract base class for clients.
    Defines interface that client may provide.
    Control class calls on these interfaces to create menace.
"""

class Client:
    def __init__(self, instances, menaces, processes, freq, freq_unit):
        self["instances"] = instances
        self["menaces"] = menaces
        self["frequency"] = freq
        self["freq_unit"] = freq_unit
        self["processes"] = processes
        self["process2inst"] = {}
        self["id2inst"] = {}

        for inst in instances:
            self["id2inst"][inst["id"]] = inst

    def kill_instance(self, instaceId):
        raise NotImplementedError

    def kill_volume(self, instanceId):
        raise NotImplementedError

    def list_instances(self):
        raise NotImplementedError

    def list_volumes(self):
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
