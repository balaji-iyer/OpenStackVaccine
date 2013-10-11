"""
    Utility functions called from various scripts.
"""
import sys
def get_module(module, frm):
    #See if module is already imported
    if "%s.%s" %(frm, module) in sys.modules:
        return getattr(sys.modules[frm], module)
    try:
        __import__(frm, fromlist=[module])
    except ImportError:
        assert True, "Couldn't import modules %s from %s" % (module, frm)
