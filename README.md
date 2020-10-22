# cadabra2-jupyter: Proof-of-Concept

## Setup
### SWIG
The `client_server` directory corresponds to the `client_server` directory in the main [cadabra2 repository](https://github.com/kpeeters/cadabra2). It contains the SWIG wrapper code and relevant CMake files, such that by modification of the root cadabra2 `CMakeLists.txt` with the addition of
```
# jupyter
add_subdirectory(client_server/jupyter)
```
the build process is fully self contained, adding the Make command
```bash
make cadabra_translator
```

To finalise the install, navigate to `build/client_server/jupyter/swig` and execute
```
pip install .
```
to copy the binaries and python scripts into the relevant module path.

### Kernel
The kernel can be installed with
```bash
pip install . && jupyter kernelspec install cadabra2jupyter
```
This will be wrapped into a single `pip` command, but I am yet to find an elegant way of installing kernels with just pip.

After installation, starting a new notebook will list `Cadabra2` as an available Kernel.

## Details and features
### SWIG Wrapper
All the SWIG wrapper is doing is exposing the `cadabra::cdb2python_string` method from `core/CdbPython.hh`, such that the kernel class is able to translate cadabra code on the fly. This could easily be achieved with the already existing pybind11 wrapping, however I am unfamiliar with pybind11, so for the PoC chose a method I am confident with.

### Kernel
The kernel is an extension of the `ipykernel.kernelbase.Kernel` baseclass, and so requires very little work to bring to a functional state. It functions by routing execution calls to a context-managed `exec` call. Some vulnerabilities exist with this, but no more than with the current `pybind11::exec` call, and could be reworked to be more appropriately sandboxed if required.

To keep namespace pollution to a minimal, the context relevant execution code is contained in a separate module, which imports all of `cadabra2_default.py`, and exploits the `print` functionality of the default `Server` class defined within.

All `stdout` and `stderr` is captured, and then returned to the kernel to be filtered and dispatched to the user.

As such, this kernel implementation gains a few bonuses over the current Xeus implementation 'for-free':

- syntax highlighting for python
- filtered error and output
- portability
- sequential code execution

There exists a bug in the Xeus kernel, that if cells are ran too quickly, or with the "restart and run all" button, the order of execution is not defined, and may result in undesired behaviour.

The kernel is currently lacking

- differentiating output, i.e. rendering images/code
- resolving `::LaTeXForm` symbols (I can't see how that was done in Xeus)
