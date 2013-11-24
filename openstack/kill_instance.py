from menace import Menace
class KillInstance(Menace):
    """ Openstack kill instance menace implementation.
    """

    def can_apply(self):
        return self.instance != None

    def apply(self):
        status = True
        assert self.instance != None
        if self.client.is_owned_instance(self.instance):

            try:
                self.instance.stop_instance()
            except:
                try :
                    self.instance.pause_instance()
                except:
                    status = False
        return status




    def undo(self):
        assert self.instance != None
        status = True
        if self.client.is_owned_instance(self.instance):
            status = self.instance.get_status()
            try:
                if status == "SHUTOFF":
                    self.instance.start_instance()
                elif status == "PAUSED":
                    self.instance.resume_instance()
            except:
                status = False
        return status


