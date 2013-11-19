import importlib
import os
class Registrar:
    """ Registers various clients and menaces.
        Stores them in a key-value store.
    """

    def __init__(self, conf):
        assert "dir" in conf, \
                "dir missing from client conf. Please check configs/clients.json"

        assert "owner" in conf, \
                "owner field needed in client conf. Please check configs/clients.json"

        self.client = None
        self.name = conf.name
        self.client_dir = conf.dir
        self.owner = {
                        owner: conf.owner
                        }

        if "email" in conf:
            self.owner["email"] = conf.email

        if "mobile" in conf:
            self.owner["mobile"] = conf.mobile

        if "menaces" in conf:
            self.menaces = conf.menaces

        if "processes" in conf:
            self.processes = conf.processes

        try:
            client_mod = __import__(self.client_dir.replace("/", "."))
        except ImportError:
            print "Please check dir path. Ensure it has __init__.py file"
            sys.exit(-1)

        self.client = client_mod.get_client(self.menaces, self.processes)


    def get_client(self):
        assert client != None, \
                "Something went wrong. Client not inited. Quitting"

        return self.client

