class Menace:
    """ Abstract menace class.
        Serves as base class for all menace types.
        Define interface for menaces which client can call.
    """
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.process = None
        self.instance = None
        self.volume = None

    def can_apply(self):
        """ Decides whether or not this type of menace is applicable to client
        """
        raise NotImplementedError;

    def apply(self):
        """ Applies the menace to the client. Implemented by the derived class.
        """
        raise NotImplementedError;

    def needs_process(self):
        """ Is this menace dependent on process.
        """
        return False

    def needs_volume(self):
        """ Is this menace dependent on volume.
        """
        return False

    def undo(self):
        raise NotImplementedError;

    def get_name(self):
        return self.name

    def set_process(self, process):
        self.process = process

    def set_instance(self, instance):
        self.instance = instance

    def set_volume(self, volume):
        self.volume = volume
