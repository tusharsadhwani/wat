import json
import os.path
import sys
from importlib.abc import Loader, MetaPathFinder
import importlib.util

class JsonLoader(Loader):
    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(module.__name__ + '.json') as input_file:
            module.json = json.load(input_file)

class JsonDataLoader(Loader):
    def __init__(self, json_module) -> None:
        self.json_module = json_module

    def create_module(self, spec):
        return self.json_module.json

    def exec_module(self, module):
        pass

class JsonFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.endswith('.json'):
            json_module_name = fullname.removesuffix('.json')
            json_module = sys.modules[json_module_name]
            return importlib.util.spec_from_loader(fullname, JsonDataLoader(json_module))

        if os.path.exists(fullname + ".json"):
            return importlib.util.spec_from_loader(fullname, JsonLoader(), is_package=True)

sys.meta_path.append(JsonFinder())
