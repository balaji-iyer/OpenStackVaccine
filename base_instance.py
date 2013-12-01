import os
import paramiko
class BaseInstance:
    """ Abstract instance class.
        To be subclassed by each clienttype eg. OpenstackInstance.
        Defines basic functions used by menace class to create failure scenarios.
    """
    def __init__(self, client, server, ssh_info=None):
        self.client = client
        self.server = server
        self.ssh_info = ssh_info
        self.ssh = None
        self.sftp = None
        self.hostname = None

    def init_connection(self):

        if (self.ssh != None and
                self.sftp != None):
            return 

        key_file = self.ssh_info.get("key_file", None)
        port = self.ssh_info.get("port", None)
        username = self.ssh_info.get("username", None)
        hostname = self.get_hostname()

        # Get Private Key from SSH_INFO
        mykey = None
        if key_file:
            privatekeyfile = os.path.expanduser(key_file)
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)

        # Init SSH Client
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, username=username, pkey=mykey)
        
        # Init SFTP Client
        self.sftp = None

        if hostname != None and port != None:

            transport = paramiko.Transport((hostname, 22))
            transport.connect(username=username, pkey=mykey)
            self.sftp = paramiko.SFTPClient.from_transport(transport)

        # Setup Server Dir
        self.server_dir = self.ssh_info.get("server_dir", None)

    def get_name(self):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def fail_volume(self):
        raise NotImplementedError

    def crash_CPU(self):
        raise NotImplementedError

    def crash_IO(self):
        raise NotImplementedError

    def can_kill_process(self, process):
        raise NotImplementedError

    def get_processes(self):
        raise NotImplementedError

    def __detach_volume(self):
        raise NotImplementedError

    def add_process(self):
        raise NotImplementedError

    def remove_process(self):
        raise NotImplementedError

    def get_attached_volumes(self):
        raise NotImplementedError

    def __reattach_volume(self):
        raise NotImplementedError

    def get_client(self):
        return self.client

    def get_hostname(self):
        raise NotImplementedError
