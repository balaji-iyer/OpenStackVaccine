from base_instance import BaseInstance
import paramiko
import logging
import sys
import os

class Instance(BaseInstance):
    def __init__(self, server, ssh_info=None):
        BaseInstance.__init__(self, server, ssh_info)


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

    def _copy_script(self, script_name):
        client_script_path = os.path.join(os.getcwd(), "openstack", "scripts", "%s.sh" % script_name)
        server_script_path = os.path.join(self.server_dir, "%s.sh" % script_name)
        try:
            self.sftp.put(client_script_path, server_script_path)
        except:
            logging.error("SCP to server failed: %s" % script_name)
            sys.exit(-1)
        return server_script_path

    def exec_script(self, script_name):

        # Init connection if not up already
        self.init_connection()

        # Copy the script from this machine to target machine.
        server_script_path = self._copy_script(script_name)

        # Execute the new script
        ssh_stdin = None
        ssh_stdout = None
        ssh_stderr = None
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("/bin/bash %s" % server_script_path)
        except:
            logging.error("Script execution %s on server %s(%s) failed" % (server_script_path, self.get_name(), self.get_id()))
            sys.exit(1)
        return not ssh_stderr



    def get_hostname(self):
        if not self.hostname:
            # Get user Ip/Hostname
            assert self.server != None
            addrs  = self.server.addresses
            p_addrs = addrs.get("private", None)
            if p_addrs == None or len(p_addrs) == 0:
                logging.error("No public address attached to server %s(%s)" % (self.get_name(), self.get_id()))
                sys.exit(-1)

            for addr in p_addrs:
                if addr.get("OS-EXT-IPS:type", None) == "floating":
                    self.hostname = addr["addr"]
                    break
        return self.hostname
