from menace import Menace
import logging

class KillProcess(Menace):
    """ Openstack implementation of kill process menace.
        Kill the process passed by the scheduler if running.
    """

    def can_apply(self):
        return (self.instance != None and
                self.client.is_owned_instance(self.instance) and
                self.process != None and
                self.process in self.client.get_registered_processes())


    def needs_process(self):
        return True

    def apply(self):
        status = True
        assert self.instance != None
        assert self.process != None
        try:
            status = self.instance.kill_process(self.process)
        except:
            logging.error("Failed to kill process %s on instance %s(%s)" % (self.process, self.instance.get_name(), self.instance.get_id()))
            status = False
        return status
