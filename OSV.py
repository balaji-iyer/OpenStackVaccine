from controller.registrar import Registrar
from controller.selector import Selector
from controller.scheduler import Scheduler
from optparse import OptionParser
from recorder.recorder import Recorder
import os
import sys

CLIENTS_FILE="./configs/client.json"
class OpenStackVaccine:
    def __init__(self, conf):
        self.registrar = Registrar(conf)
        self.selector = Selector()
        self.scheduler = Scheduler(conf)
        self.recorder = Recorder()


if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("-c", "--client", dest="client", type="string")
        (options, args) = parser.parse_args()

        client_file = open(CLIENTS_FILE)
        clients_json = json.load(client_file)

        client = None

        for client_json in client_json:
            if options.client == client_json.name:
                client = client_json

        if client == None:
            print "Client %s not found. Check clients.json file" % option.client
            sys.exit(-1)
        
        ovs = OpenStackVaccine(client)
