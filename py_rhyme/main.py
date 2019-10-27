from .helpers import _dataset


class PyRhyme:
    """
    Reading and maniputaling Rhyme chombo outputs
    """

    def __init__(self, path):
        """
        Initializing a PyRhyme object by:
        - opening a dataset
        - loading the specified chombo file
        """

        self.d = _dataset._open(path)
