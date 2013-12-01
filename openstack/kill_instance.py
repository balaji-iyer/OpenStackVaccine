from menace import Menace
import logging
class KillInstance(Menace):
    """ Openstack kill instance menace implementation.
    """

    def can_apply(self):
        return (self.instance != None and 
                self.client.is_owned_instance(self.instance))

    def apply(self):
        status = True
        assert self.instance != None
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
        inst_status = self.instance.get_status()
        try:
            if inst_status == "SHUTOFF":
                self.instance.start_instance()
            elif inst_status == "PAUSED":
                self.instance.resume_instance()
            logging.info("Restarting instance %s(%s)" % (self.instance.get_name(), self.instance.get_id()))
        except:
            status = False
        return status

