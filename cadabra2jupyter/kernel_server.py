class KernelServer:
    def __init__(self, kernel_instance):
        self._kernel = kernel_instance

    def send(self, data, typestr, parent_id, last_in_sequence):
        """Send a message to the client; 'typestr' indicates the cell type,
        'parent_id', if non-null, indicates the serial number of the parent
        cell.
        """
        if typestr == "latex_view":
            data = data.replace("\\begin{dmath*}", "$").replace("\\end{dmath*}", "$")
            self._kernel._send_result(data)
        elif typestr == "image_png":
            # todo
            self._kernel._send_image(data)
        elif typestr == "verbatim":
            self._kernel._send_code(data)
        elif typestr == "input_form":
            #  pass
            ...
        else:
            raise Exception("Unknown typestr '{}'".format(typestr))
        return 0

    def architecture(self):
        return "jupyter-kernel"

    def test(self):
        self._kernel._send_result("Test: We've gone on holiday by mistake!")

    def handles(self, otype):
        if otype == "latex_view" or otype == "image_png" or otype == "verbatim":
            return True
        return False

    def totals(self):
        # what does this do?
        return -1
