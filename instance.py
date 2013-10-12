"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
import util

class Instance:
    def __init__(self):
        # Load module novaclient in unix system
        try:
            cmd = os.popen("module load novaclient")
            exec(cmd)
        except:
            assert "module novaclient could not be loaded"

        if not os.path.isfile("~/.futuregrid/novarc"):
            try:
                cmd = os.popen("module load cloudmesh")
                exec(cmd)
            except:
                assert "cloudmesh not loaded"
            try:
                cmd2 = os.popen("cm-manage config sierra-openstack-grizzly")
                exec(cmd2)
            except:
                assert "novarc not created"


        # import novaclient in python
        try:
            client = util.get_module("novaclient", "client")
        except Exception:
            assert "novaclient module cannot be loaded"

if __name__ == "__main__":
    instance = Instance();
