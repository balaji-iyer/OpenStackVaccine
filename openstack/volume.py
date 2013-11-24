from base_volume import BaseVolume

class Volume(BaseVolume):
    def __init__(self, instance, volume):
        BaseVolume.__init__(self, instance, volume)

    def get_device(self):
        return self.volume.device

    def get_id(self):
        return self.volume.VolumeId

    def get_instance_id(self):
        return self.instance.get_id()


