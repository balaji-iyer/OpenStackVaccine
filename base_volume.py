class BaseVolume:
    """ Abstract volume class
        To be subclassed by each client type. Ex. OpenstackVolume.
        Define helper functions and getters and setter for menace activities.
    """

    def __init__(self, instance, volume):
        self.instance = instance
        self.volume = volume

    def get_device(self):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def get_instance_id(self):
        raise NotImplementedError

