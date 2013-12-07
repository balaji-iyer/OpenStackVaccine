from menace import Menace
import logging
class CrashCpu(Menace):
    """ Openstack implementation of Crash CPU
        Runs 32 threads on heavy task to burn out cpu.
    """

    def can_apply(self):
        return (self.instance != None and
                self.client.is_owned_instance(self.instance))


    def apply(self):
        assert self.instance != None
        status = True
        try:
            self.instance.exec_script("crash_cpu")
        except:
            logging.error("Executing menace %s failed" % "crash_cpu")
            status = False

        return status

    def undo(self):
        assert self.instance != None
        status = False
        try:
            status = self.instance.exec_script("crash_cpu_undo")
        except:
            logging.error("Executing menace %s failed" % "crash_cpu")

        return status
