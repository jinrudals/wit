#!/usr/bin/env python3

import json
from lib.package import Package
from collections import OrderedDict
import logging

log = logging.getLogger('wit')


# TODO
# Should we use different datastructures?
# The JSON file format slightly differs from manifest, why?
class LockFile:
    """
    Common class for the description of package dependencies and a workspace
    """

    def __init__(self, packages=[]):
        self.packages = packages

    def contains_package(self, package):
        for p in self.packages:
            if p.name == package.name:
                return True
        return False

    def add_package(self, package):
        self.packages.append(package)

    def write(self, path):
        log.debug("Writing lock file to {}".format(path))
        contents = OrderedDict((p.name, p.manifest()) for p in self.packages)
        manifest_json = json.dumps(contents, sort_keys=True, indent=4) + '\n'
        path.write_text(manifest_json)

    @staticmethod
    def read(path):
        log.debug("Reading lock file from {}".format(path))
        content = json.loads(path.read_text())
        wsroot = path.parent
        return LockFile.process(wsroot, content)

    @staticmethod
    def process(wsroot, content):
        packages = [Package.from_manifest(wsroot, x) for _, x in content.items()]
        return LockFile(packages)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
