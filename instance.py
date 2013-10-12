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
        # import novaclient in python
        try:
            client = util.get_module("client","novaclient")
        except Exception:
            assert "novaclient module cannot be loaded"

if __name__ == "__main__":
    instance = Instance();
