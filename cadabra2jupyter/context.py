"""
Proof-of-Concept cadabra2 jupyter kernel
"""
from io import StringIO
import sys, os
import cadabra2

# super important
__cdbkernel__ = cadabra2.__cdbkernel__

# needs dynamic configuration; cmake?
SITE_PATH = "/usr/local/lib/python3.8/site-packages"

server = None  #  require so that server is in global namespace

#  import cadabra2 defaults programatically so it shares global namespace
with open(os.path.join(SITE_PATH, "cadabra2_defaults.py")) as f:
    code = compile(f.read(), "cadabra2_defaults.py", "exec")
exec(code, globals())


def _attatch_kernel_server(instance):
    global server
    server = instance


def _exec_in_context(code):
    exec(code, globals())
