"""
Script accomplishes the following tasks.
    1. Init environment on seirra.futuregrid.org
    2.
"""
import os
import sys
import subprocess
import util

class Instance:
    def __init__(self):
        # Load module novaclient in unix system
        if 0 != subprocess.call("module load novaclient"):
            assert "module novaclient could not be loaded"

        # import novaclient in python
        try:
            client = util.get_module("novaclient", "client")
        except Exception:
            assert "novaclient module cannot be loaded"

if __name__ == "__main__":
    instance = Instance();
