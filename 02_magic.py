import sys
from importlib.abc import Loader, MetaPathFinder
import importlib.util

class MagicLoader(Loader):
    def create_module(self, spec):
        return 42

    def exec_module(self, module):
        pass

class MagicFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        # To avoid startup code breakage
        if fullname == 'atexit': return None

        return importlib.util.spec_from_loader(fullname, MagicLoader())

sys.meta_path.insert(0, MagicFinder())
