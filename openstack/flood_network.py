from menace import Menace
import logging

class FloodNetwork(Menace):
    """ Openstack implementation of Flood Network.
        Adds 1000ms delay to each packet to simulate heavy congestion in traffic.
    """

    def can_apply(self):
        return (self.instance != None and
                self.client.is_owned_instance(self.instance))


    def apply(self):
        assert self.instance != None
        status = False
        try:
            status = self.instance.exec_script("flood_network")
        except:
            logging.error("Executing menace %s failed" % "flood_network")

        return status
