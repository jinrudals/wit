#!/usr/bin/env python3

import argparse
import lib.gitrepo
import lib.git_package
import lib.workspace
import os
from pathlib import Path


# Make this a factory for different VCS types
class Package:
    """
    Generic package type
    """

    @staticmethod
    def from_arg(s):
        """
        >>> Package.from_arg(".::HEAD")
        lib.gitrepo.GitRepo(source='.', revision='HEAD')
        >>> Package.from_arg("not-a-repo")
        Traceback (most recent call last):
            ...
        argparse.ArgumentTypeError: Remote git repo 'not-a-repo' does not exist!
        """
        # TODO Could speed up validation
        #   - use git ls-remote to validate remote exists
        #   - use git ls-remote to validate revision for tags and branches
        #   - if github repo, check if page exists (or if you get 404)
        # FIXME: This is ugly. Split on '::' into a path and revision, but
        # there may not be a revision. So add an additional array
        source, rev = (s.split("::") + [None])[:2]
        if rev is None:
            rev = "HEAD"
        if not lib.gitrepo.GitRepo.is_git_repo(source):
            msg = "Remote git repo '{}' does not exist!".format(source)
            raise argparse.ArgumentTypeError(msg)

        name = lib.gitrepo.GitRepo.remote_to_name(source)
        return lib.git_package.GitPackage(rev, name, source)

    @staticmethod
    def from_manifest(m):
        commit = m['commit']
        name = m['name']
        source = m['source']

        return lib.git_package.GitPackage(commit, name, source)

    @staticmethod
    def from_cwd():
        cwd = Path(os.getcwd()).resolve()

        # walk up the path until the /parent/ directory contains a wit
        # manifest file
        for p in ([cwd] + list(cwd.parents)):
            if lib.workspace.WorkSpace.is_workspace(p / '..'):
                return lib.gitrepo.GitRepo(str(p), None, wsroot=(p / '..').resolve())

        return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
