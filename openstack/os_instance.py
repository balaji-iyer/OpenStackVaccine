from clients import instance


class OS_Instance(Instance):
    def __init__(self):
        Instance.__init__(self, instance_id, floating_ip, fixed_ip, volumes, name)


