from controller.registrar import Registrar
import json

class TestRegistrar:
    def __init__(self, conf, auth_info):
        self.registrar = Registrar(conf, auth_info)

    def test_client(self):
        assert self.registrar.client != None

        assert self.registrar.client != None
        print self.registrar.client.handle.flavors.list()

    def test_owner(self, conf):
        owner = self.registrar.owner

        assert owner["name"] == conf["owner"]
        print "name:\t%s" % owner["name"]
        if "email" in conf:
            assert owner["email"] == conf["email"]
            print "email:\t%s" % owner["email"]

        if "mobile" in conf:
            assert owner["mobile"] == conf["mobile"]
            print "mobile:\t%s" % owner["mobile"]


if __name__ == "__main__":
    conf_file = open("../config/clients.json")
    conf_json = json.load(conf_file)

    client = conf_json[0]

    auth_info = json.load(open("../config/auth.json"))[client["name"]]
    test = TestRegistrar(client, auth_info)

    test.test_client()
    test.test_owner(client)
