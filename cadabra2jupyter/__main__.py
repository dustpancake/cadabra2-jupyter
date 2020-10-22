"""
Proof-of-Concept cadabra2 jupyter kernel
"""
from ipykernel.kernelapp import IPKernelApp
from cadabra2jupyter.kernel import CadabraJupyterKernel

if __name__ == "__main__":
    IPKernelApp.launch_instance(kernel_class=CadabraJupyterKernel)
