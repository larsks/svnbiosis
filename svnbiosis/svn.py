#!/usr/bin/python

import os
import sys
import subprocess
import errno

from distutils.file_util import copy_file

class SvnError (Exception):
    pass

class RepositoryCreateFailed (SvnError):
    pass

class Repository (object):
    def __init__ (self, repo, wc=None):
        self.repo = repo

        if wc:
            self.wc = wc
        else:
            self.wc = os.path.basename(repo)

    def uri(self):
        return 'file://' + os.path.abspath(self.repo)

    def checkout(self, wc=None):
        if wc:
            self.wc = wc

        rc = subprocess.call(['svn', 'co', self.uri(), self.wc])

    def update(self):
        rc = subprocess.call(['svn', 'update', '--quiet', self.wc])

    def add(self, files):
        rc = subprocess.call(['svn', 'add'] + files)

    def commit(self, message):
        rc = subprocess.call(['svn', 'commit', '-m', message,
            self.wc])


def createRepository(repo, conf=None, hooks=None):
    rc = subprocess.call(['svnadmin', 'create', repo])
    if rc != 0:
        raise RepositoryCreateFailed('Failed with exitcode = %d' % rc)

    if hooks:
        for name, path in hooks.items():
            os.symlink(path,
                    os.path.join(repo, 'hooks', name))

    if conf:
        for name, path in conf.items():
            try:
                os.unlink(
                        os.path.join(repo, 'conf', name))
            except OSError, detail:
                if detail.errno != errno.ENOENT:
                    raise

            os.symlink(path,
                    os.path.join(repo, 'conf', name))

    return Repository(repo)

