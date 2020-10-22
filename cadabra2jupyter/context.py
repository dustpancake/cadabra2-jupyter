"""
Proof-of-Concept cadabra2 jupyter kernel
"""
from cadabra2_defaults import *
from io import StringIO
import sys

# super important
__cdbkernel__ = cadabra2.__cdbkernel__


class _RedirectionContextFactory:
    def __init__(self):
        self.codeOut = StringIO()
        self.codeErr = StringIO()

    def __enter__(self):
        sys.stdout = self.codeOut
        sys.stderr = self.codeErr

    def __exit__(self, exc_type, exc_val, exc_traceback):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def get(self):
        return self.codeOut.getvalue(), self.codeErr.getvalue()


def exec_in_context(code):
    # faster to create new StringIO on each call rather than to clear
    _redirectcontext = _RedirectionContextFactory()

    with _redirectcontext:
        exec(code, globals())

    return _redirectcontext.get()
