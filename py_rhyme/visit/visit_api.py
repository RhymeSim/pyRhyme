import subprocess, os, sys


class VisitAPI:
    """
    VisIt python package to generate different plots based on Rhyme chombo outpus
    """

    def __init__(self, visit_lib_dir=None):
        """
        Initializing a VisitAPI object

        Parameter
        visit_lib_dir: Path to VisIt python packages directory
        """

        if visit_lib_dir is None:
            visit_lib_dir = '/opt/visit/current/linux-x86_64/lib/site-packages'

        if os.path.exists(visit_lib_dir):
            if visit_lib_dir not in sys.path:
                sys.path.append(visit_lib_dir)
        else:
            raise RuntimeError(visit_lib_dir, 'does not exists')

        import visit

        self.ds = {
            'path': ''
        }


        def load(self, path):
            """
            Loading one or a sequence of chombo files

            Parameter
            path: Path to chombo file(s)
                Use globbing to open a sequence of files
                e.g. /path/to/result_*.chombo.h5
            """
            pass
