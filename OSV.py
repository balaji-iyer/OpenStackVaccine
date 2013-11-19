from controller.registrar import Registrar
from recorder.recorder import Recorder
from controller.selector import Selector
from controller.scheduler import Scheduler
from optparse import OptionParser
import json
import os
import sys

CLIENTS_FILE = "./config/clients.json"
AUTH_FILE = "./config/auth.json"

class OpenStackVaccine:
    def __init__(self, conf, auth_info):
        self.registrar = Registrar(conf, auth_info)
        self.selector = Selector(self.registrar.client)
        self.scheduler = Scheduler(conf)
        self.recorder = Recorder()


if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("-c", "--client", dest="client", type="string")
        (options, args) = parser.parse_args()

        client_file = open(CLIENTS_FILE)
        clients_json = json.load(client_file)

        client = None

        for client_json in clients_json:
            if options.client == client_json["name"]:
                client = client_json

        if client == None:
            print "Client %s not found. Check clients.json file" % options.client
            sys.exit(-1)

        # Getting auth info for the client
        auth_file = open(AUTH_FILE)
        auth_json = json.load(auth_file)

        if client["name"] not in auth_json:
            print "Auth Info not found in auth.json for client %s" % options.client
            sys.exit(-1)

        auth_info = auth_json[client["name"]]
        osv = OpenStackVaccine(client, auth_info)

        import pdb;pdb.set_trace()
        osv.scheduler.start(osv)

