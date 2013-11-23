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
    def __init__(self, debug=False):
        self.debug = debug


    def select_menace(self, osv):
        menaces = osv.registrar.get_menaces()
        if menaces == None or len(menaces) == 0:
            logging.error("Menace list missing. Check clients.json")
            sys.exit(-1)
        (menace_name, menace_cls) = self._select_random(menaces)
        logging.info("Selecting Menace: %s" % menace_name)

        # Instantiate class and return object
        client = osv.registrar.get_client()
        return menace_cls(menace_name, client)


    def select_instance(self, osv):
        client = osv.registrar.get_client()
        instances = client.list_instances()

        if instances == None or len(instances) == 0:
            logging.error("No instance up right now. Nothing to do")
            # Donot kill, servers might come up eventually
            return None

        instance = self._select_random(instances)
        logging.info("Selecting Instance: %s" % instance.id)
        return instance

    def select_process(self, osv):
        client = osv.registrar.get_client()

        processes = client.processes
        if processes == None or len(processes) == 0:
            logging.error("Process list missing. Check clients.json")
            sys.exit(-1)

        process = self._select_random(processes)
        logging.info("Selecting process: %s" % process)
        return process

    def select_volume(self, osv):
        pass

    def _select_random(self, list):
        index = int(random.uniform(0, len(list)))
        return list[index]
