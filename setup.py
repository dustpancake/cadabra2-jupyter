from setuptools import setup, find_packages
from setuptools.command.install import install
from jupyter_client.kernelspec import install_kernel_spec


class KernelInstall(install):
    def run(self):
        install.run(self)
        install_kernel_spec("kernel", kernel_name="Cadabra2")


setup(
    name="cadabra2-jupyter",
    description="Cadabra2 Proof-of-Concept Jupyter Kernel",
    author="Fergus Baker",
    version="0.1.0",
    packages=find_packages(exclude=["client_server"]),
    cmdclass={"install": KernelInstall},
    zip_safe=False,
)
