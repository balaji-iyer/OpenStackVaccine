from controller.registrar import Registrar
from recorder.recorder import Recorder
from controller.selector import Selector
from controller.scheduler import Scheduler
from optparse import OptionParser
import json
import logging
import os
import pprint
import sys

CLIENTS_FILE = "./config/clients.json"
AUTH_FILE = "./config/auth.json"

class OpenStackVaccine:
    def __init__(self, debug):
        self.registrar = Registrar(debug)
        self.selector = Selector(debug)
        self.scheduler = Scheduler(debug)
        self.recorder = Recorder(debug)


if __name__ == "__main__":
    parser = OptionParser()
    logging.basicConfig(level=logging.INFO)
    parser.add_option("-c", "--client", dest="client", type="string")
    parser.add_option("-d", "--debug", dest="debug", action="store_true")
    (options, args) = parser.parse_args()

    logging.info("Running OpenStackVaccine for client %s" % options.client)
    conf_file = open(os.path.abspath(CLIENTS_FILE))
    clients_json = json.load(conf_file)

    conf = None

    for client_json in clients_json:
        if options.client == client_json["name"]:
            conf = client_json
            logging.info("Client Info:%s", json.dumps(conf, sort_keys=True, indent=4))

    if conf == None:
        logging.error("Client %s not found. Check clients.json file" % options.client)
        sys.exit(-1)

    # Getting auth info for the client
    auth_file = open(os.path.abspath(AUTH_FILE))
    auth_json = json.load(auth_file)

    if conf["name"] not in auth_json:
        logging.error("Auth Info not found in auth.json for client %s" % options.client)
        sys.exit(-1)

    auth_info = auth_json.get(conf["name"])
    logging.info("Auth Info:%s" % json.dumps(auth_info, sort_keys=True, indent=4))
    pprint.pprint(auth_info)

    osv = OpenStackVaccine(options.debug)

    osv.registrar.register_owner(conf["owner"])
    osv.registrar.register_client(conf["name"], conf["dir"], conf["client"], auth_info)
    osv.registrar.register_menaces(conf["dir"], conf["client"])
    osv.registrar.register_notifier(options.client, conf["notifier"], conf["owner"])


    osv.scheduler.start(osv, conf.get("schedule", {}))
