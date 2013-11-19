from menace import Menace
import random
import sys

class Selector:
    """ Selector class.
        Decides upon which type of menace to make.
        Which instances to make this menace on.
        If process or volume related, returns a random
        process or volume too respectively.
    """
    def __init__(self, client):
        self.client = client

    def select_menace(self):
        menaces = self.client.menaces
        if menaces == None or len(menaces) == 0:
            print "Menace list missing. Check clients.json"
            sys.exit(-1)

        return self._select_random(menaces)


    def select_instance(self):
        instances = self.client.list_instances()

        if instances == None or len(instances) == 0:
            print "No instance up right now. Nothing to do"
            return None
        return self._select_random(instances)

    def select_process(self, menace):

        if menace != Menace.KILL_PROCESS:
            print "Wrong menace type: %s" % menace
            sys.exit(-1)

        processes = self.client.processes
        if processes == None or len(processes) == 0:
            print "Process list missing. Check clients.json"
            sys.exit(-1)

        return self._select_random(processes)


    def select_volume(self, client, instance):
        pass

    def _select_random(self, list):
        index = int(random.uniform(0, len(list)))
        return list[index]
