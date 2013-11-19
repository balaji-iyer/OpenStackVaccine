from os_client import OS_Client

def get_client(menaces, processes, auth_info):
    return OS_Client(menaces, processes, auth_info)
