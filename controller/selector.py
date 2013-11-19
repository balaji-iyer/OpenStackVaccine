from menace import Menace
import random
import sys
import logging

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
            logging.error("Menace list missing. Check clients.json")
            sys.exit(-1)
        menace = self._select_random(menaces)
        logging.info("Selecting Menace: %s" % menace)
        return menace


    def select_instance(self):
        instances = self.client.list_instances()

        if instances == None or len(instances) == 0:
            logging.error("No instance up right now. Nothing to do")
            # Donot kill, servers might come up eventually
            return None

        instance = self._select_random(instances)
        logging.info("Selecting Instance: %s" % instance.id)
        return instance

    def select_process(self, menace):

        if menace != Menace.KILL_PROCESS:
            logging.error("Wrong menace type: %s" % menace)
            sys.exit(-1)

        processes = self.client.processes
        if processes == None or len(processes) == 0:
            logging.error("Process list missing. Check clients.json")
            sys.exit(-1)

        process = self._select_random(processes)
        logging.info("Selecting process: %s" % process)

    def select_volume(self, client, instance):
        pass

    def _select_random(self, list):
        index = int(random.uniform(0, len(list)))
        return list[index]
