"""
    Abstract base class for clients.
    Defines interface that client may provide.
    Control class calls on these interfaces to create menace.
"""

class Client:
    def __init__(self):
        pass

    def terminate_instance(self, instaceId):
        pass

    def delete_volume(self, volumeId):
        pass

    def list_instances(self):
        pass

    def list_volumes(self):
        pass

    def kill_process(self, instanceId, processId):
        pass
