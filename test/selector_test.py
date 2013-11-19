from controller.selector import Selector
from controller.registrar import Registrar
from menace import Menace
import json


class TestSelector:
    def __init__(self, client):
        self.client = client
        self.selector = Selector(client)

    def test_select_menace(self):
        menace = self.selector.select_menace()
        assert menace in self.client.menaces
        print menace

    def test_select_instace(self):
        instance = self.selector.select_instance()
        assert instance in self.client.list_instances()
        print instance

    def test_select_process(self):
        process = self.selector.select_process(Menace.KILL_PROCESS)
        assert process in self.client.processes
        print process


if __name__ == "__main__":
    conf_file = open("../config/clients.json")
    conf_json = json.load(conf_file)

    client = conf_json[0]

    auth_info = json.load(open("../config/auth.json"))[client["name"]]
    registrar = Registrar(client, auth_info)

    test = TestSelector(registrar.client)
    test.test_select_menace()
    test.test_select_instace()
    test.test_select_process()

