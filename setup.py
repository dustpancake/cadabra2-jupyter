from setuptools import setup, find_packages

setup(
    name="cadabra2-jupyter",
    description="Cadabra2 Proof-of-Concept Jupyter Kernel",
    author="Fergus Baker",
    version="0.1.0",
    packages=find_packages(exclude=["client_server"]),
    zip_safe=False,
)
