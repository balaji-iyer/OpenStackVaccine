from menace import Menace

class KillInstance(Menace):

    def can_apply(self):
        return True

    def apply(self, instance, process, volume):
        status = True
        if self.client.is_owned_instance(instance):
            try:
                self.client.stop_instance(instance)
            except:
                try :
                    self.client.pause_instance(instance)
                except:
                    status = False
        return status



    
    def undo(self, instance, process, volume):
        status = True
        if self.client.is_owned_instance(instance):
            try: 
                if instance.status == "SHUTOFF":
                    self.client.start_instance()
                elif instance.status == "PAUSED":
                    self.client.resume_instance()
            except:
                status = False
        return status


