from menace import Menace
import logging

class FailDns(Menace):
    """ Openstack implementation of Fail DNS.
        Changes iptables rule to drop tcp and udp packets on port 53.
    """

    def can_apply(self):
        return (self.instance != None and
                self.client.is_owned_instance(self.instance))


    def apply(self):
        assert self.instance != None
        status = True
        try:
            self.instance.exec_script("fail_dns")
        except:
            status = False
            logging.error("Executing menace %s failed" % "fail_dns")

        return status
