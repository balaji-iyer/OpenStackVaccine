"""
    Abstract instance class.
    To be subclassed by each clienttype eg. OpenstackInstance.
    Defines basic functions used by menace class to create failure scenarios.
"""

class Instance:
    def __init__(self, instance_id, floating_ip, fixed_ip, volumes, name):
        self.id = instance_id
        self.floating_ip = floating_ip
        self.fixed_ip = fixed_ip
        self.name = name
        self.volumes = volumes


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

