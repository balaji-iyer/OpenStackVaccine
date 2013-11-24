from menace import Menace
import random

class FailVolume(Menace):

    def can_apply(self):
        return True

    def apply(self):
        assert self.instance != None
        assert self.volume != None
        assert self.instance.get_id() == self.volume.get_instance_id()
        self.client.kill_volume(self.volume)

    def undo(self):
        assert self.instance != None
        assert self.volume != None
        
        assert self.instance.get_id() == self.volume.get_instance_id()
        self.client._reattach_volume(self.volume)
        
