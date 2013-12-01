from menace import Menace
import logging

class FailNetwork(Menace):
    """ Openstack implementation of Fail Network.
        Drops a percentage of packets.
    """

    def can_apply(self):
        return (self.instance != None and
                self.client.is_owned_instance(self.instance))


    def apply(self):
        assert self.instance != None
        status = False
        try:
            status = self.instance.exec_script("fail_network")
        except:
            logging.error("Executing menace %s failed" % "fail_network")

        return status
