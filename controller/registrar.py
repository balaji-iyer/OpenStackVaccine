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

        self.owner = {
            "name": conf["name"]
                    }
        if "email" in conf:
            self.owner["email"] = conf["email"]

        if "mobile" in conf:
            self.owner["mobile"] = conf["mobile"]

    def register_client(self, name, dir, conf, auth_info):

        self.name = name
        self.client_dir = dir

        try:

            # SO/10675054 Notice . in front of wrapper.
            # This is to specify relative path of wrapper w.r.t package
            client = importlib.import_module(".client",
                            self.client_dir.replace("/", "."))

        except ImportError:
            logging.error("""Please check dir path.
                            Ensure it has __init__.py and
                            client.py in %s dir"""
                    % self.client_dir)
            sys.exit(-1)

        logging.info("Registering client from %s module"
                        % self.client_dir.replace("/","."))

        self.client = client.Client(self.name, conf, auth_info)

    def register_menaces(self, dir, conf):
        assert "menaces" in conf, \
                "menaces missing from client conf. Please check configs/clients.json"

        menaces = conf.get("menaces", [])

        if menaces != None:
            for menace in menaces:
                try:
                    module = importlib.import_module(".%s" % menace,
                            dir.replace("/", "."))

                except ImportError:
                    logging.error("Please check dir path. Ensure it has __init__.py and %s.py" % menace)
                    sys.exit(-1)

                menace_cls_name = menace.title().replace("_", "")
                logging.info("Registering %s menace"
                                % menace_cls_name)

                try:
                    menace_cls = getattr(module, menace_cls_name)
                except AttributeError:
                    logging.info("%s menace module should contain %s class"
                            % (menace, menace_cls_name))
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
