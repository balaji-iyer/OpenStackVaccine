class BaseInstance:
    """ Abstract instance class.
        To be subclassed by each clienttype eg. OpenstackInstance.
        Defines basic functions used by menace class to create failure scenarios.
    """
    def __init__(self, server):
        self.server = server

    def get_name(self):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def fail_volume(self):
        raise NotImplementedError

    def crash_CPU(self):
        raise NotImplementedError

    def crash_IO(self):
        raise NotImplementedError

    def can_kill_process(self, process):
        raise NotImplementedError

    def get_processes(self):
        raise NotImplementedError

    def __detach_volume(self):
        raise NotImplementedError

    def add_process(self):
        raise NotImplementedError

    def remove_process(self):
        raise NotImplementedError

    def get_attached_volumes(self):
        raise NotImplementedError

    def __reattach_volume(self):
        raise NotImplementedError

