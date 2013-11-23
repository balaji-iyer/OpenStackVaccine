import importlib
import os
import sys
import logging

class Registrar:
    """ Registers various clients and menaces.
        Stores them in a key-value store.
    """

    def __init__(self, debug):

        self.client = None
        self.owner = None
        self.menaces = []
        self.name = None
        self.client_dir = None
        self.debug = debug


    def register_owner(self, conf):
        assert "owner" in conf, \
                "owner field needed in client conf. Please check configs/clients.json"

        self.owner = {
                        "name": conf["owner"]
                        }
        if "email" in conf:
            self.owner["email"] = conf["email"]

        if "mobile" in conf:
            self.owner["mobile"] = conf["mobile"]

    def register_client(self, conf, auth_info):
        assert "dir" in conf, \
                "dir missing from client conf. Please check configs/clients.json"

        self.name = conf["name"]
        self.client_dir = conf["dir"]
        try:
            # SO/10675054 Notice . in front of wrapper.
            # This is to specify relative path of wrapper w.r.t package
            client = importlib.import_module(".client", self.client_dir.replace("/", "."))
        except ImportError:
            logging.error("Please check dir path. Ensure it has __init__.py and client.py in %s dir" % self.client_dir)
            sys.exit(-1)

        logging.info("Registering client from %s module" % self.client_dir.replace("/","."))
        self.client = client.Client(conf["menaces"], conf["processes"], auth_info)

    def register_menaces(self, conf):
        assert "menaces" in conf, \
                "menaces missing from client conf. Please check configs/clients.json"
        menaces = conf.get("menaces", [])

        if menaces != None:
            for menace in menaces:
                try:
                    module = importlib.import_module(".%s" % menace, self.client_dir.replace("/", "."))
                except ImportError:
                    logging.error("Please check dir path. Ensure it has __init__.py and %s.py" % menace)
                    sys.exit(-1)

                menace_cls_name = menace.title().replace("_", "")

                logging.info("Registering %s menace" % menace_cls_name)

                try:
                    menace_cls = getattr(module, menace_cls_name)
                except AttributeError:
                    logging.info("%s menace module sould contain %s class" % (menace, menace_cls_name))
                    sys.exit(-1)
                self.menaces.append((menace, menace_cls))

    def get_client(self):
        assert self.client != None, \
                "Something went wrong. Client not inited. Quitting"

        return self.client

    def get_owner(self):
        assert self.owner != None, \
                "Something went wrong. Owner Info not found. Quitting"
        return self.owner

    def get_menaces(self):
        if (self.menaces == None or
                len(self.menaces) == 0):
            logging.warn("No menace found")
            return []
        return self.menaces
