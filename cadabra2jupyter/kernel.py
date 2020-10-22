"""
Proof-of-Concept cadabra2 jupyter kernel
"""

import ipykernel.kernelbase
import sys
import traceback

# only additional cadabra2 C++ function that required wrapping
import cadabra_translator

from cadabra2jupyter.context import exec_in_context


class CadabraJupyterKernel(ipykernel.kernelbase.Kernel):
    implementation = "cadabra_kernel"
    implementation_version = 0.1
    language_info = {
        "name": "cadabra2",
        "codemirror_mode": "python",
        "pygments_lexer": "python",
        "mimetype": "text/python",
        "file_extension": ".ipynb",
    }

    @property
    def banner(self):
        return "Cadabra2 Jupyter Kernel {}".format(self.implementation_version)

    def __init__(self, **kwargs):
        ipykernel.kernelbase.Kernel.__init__(self, **kwargs)
        self._parse_cadabra = cadabra_translator.parse_cadabra

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        self.silent = silent

        if not code.strip():
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        interrupted = False
        try:
            pycode = self._parse_cadabra(code)
            res_out, res_err = self._execute_python(pycode)

        except KeyboardInterrupt:
            interrupted = True

        except Exception as e:
            # get traceback; not massively imformative but can be useful
            err_str = traceback.format_exc()
            self._send_error(err_str)

        else:
            # at the moment, assumes all content is LaTeX style
            #  images/plots will require another branch, and code
            # objects likewise -- most of the logic can be taken
            # from the Server.cc implementation with a little rework
            for line in res_err.split("\n"):
                if line.strip() != "":
                    self._send_error(line)

            for line in res_out.split("\n"):
                if line.strip() != "":
                    self._send_result(line)

        if interrupted:
            return {"status": "abort", "execution_count": self.execution_count}
        else:
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

    def _execute_python(self, pycode):
        """executes python code in the cadabra context
        would also in future create hooks for the return type
        i.e. images vs. LaTeX vs. code."""
        return exec_in_context(pycode)

    def _send_result(self, res_str):
        self.send_response(
            self.iopub_socket,
            "display_data",
            {"data": {"text/markdown": "${}$".format(res_str)}, "metadata": {}},
        )

    def _send_error(self, err_str):
        self.send_response(
            self.iopub_socket, "stream", {"name": "stderr", "text": err_str}
        )
