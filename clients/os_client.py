from novaclient.v1_1 import client
class OS_Client(Client):
    def __init__(self, instances, menaces, processes, freq, freq_unit, os_auth_info):
        super(self, instances, menaces, processes, freq, freq_unit)
        self["handle"] = client.Client(os_auth_info["username"],
                                       os_auth_info["tenant_name"],
                                       os_auth_info["password"],
                                       os_auth_info["auth_url"], 
                                       insecure=True,
                                       service_type="compute")


    def kill_instance(self, instanceId):
        instance = self["id2inst"].get(instanceId, None)
        if instance == None:
            raise Exception

        if not "kill_instance" in self["menaces"]:
            raise Exception

        self["handle"].server.stop(instanceId);
        
        


