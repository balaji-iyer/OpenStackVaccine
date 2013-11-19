import importlib
import os
import sys
import logging
class Registrar:
    """ Registers various clients and menaces.
        Stores them in a key-value store.
    """

    def __init__(self, conf, auth_info):
        assert "dir" in conf, \
                "dir missing from client conf. Please check configs/clients.json"

        assert "owner" in conf, \
                "owner field needed in client conf. Please check configs/clients.json"

        self.client = None
        self.name = conf["name"]
        self.client_dir = conf["dir"]
        self.owner = {
                        "name": conf["owner"]
                        }

        if "email" in conf:
            self.owner["email"] = conf["email"]

        if "mobile" in conf:
            self.owner["mobile"] = conf["mobile"]


        try:
            # SO/10675054 Notice . in front of wrapper.
            # This is to specify relative path of wrapper w.r.t package
            wrapper = importlib.import_module(".wrapper", self.client_dir.replace("/", "."))
        except ImportError:
            logging.error("Please check dir path. Ensure it has __init__.py file")
            sys.exit(-1)

        logging.info("Getting client from %s.wrapper module" % self.client_dir.replace("/","."))

        self.client = wrapper.get_client(conf["menaces"], conf["processes"], auth_info)


    def get_client(self):
        assert self.client != None, \
                "Something went wrong. Client not inited. Quitting"

        return self.client

