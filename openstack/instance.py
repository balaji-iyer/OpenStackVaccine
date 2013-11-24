from base_instance import BaseInstance

class Instance(BaseInstance):
    def __init__(self, server):
        BaseInstance.__init__(self, server)

    def get_name(self):
        return self.server.name

    def get_id(self):
        return self.server.id

    def start_instance(self):
        instance = self.server
        if (instance != None and
                instance.status != "ACTIVE"):
            instance.start()

    def resume_instance(self):
        instance = self.server
        if (instance != None and
                instance.status != "ACTIVE"):
            instance.resume()

    def stop_instance(self):
        server = self.server
        if (server != None and
                server.status == "ACTIVE"):
            server.stop();

    def pause_instance(self):
        server = self.server
        if (server != None and
            server.status == "ACTIVE"):
            server.pause()

    def get_status(self):
        return self.server.status

