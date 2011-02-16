#!/usr/bin/python

import os

if not hasattr(os.path, 'relpath'):
    import stupid
    os.path.relpath = stupid.relpath

import sys
import logging
import subprocess
import ConfigParser
import re

import app
import ssh
import svn

re_valid_repo = re.compile('^[\w\d]+$')

class Main(app.App):
    logtag = 'svnbiosis.post-commit-user'

    def handle_args(self, args):
        try:
            repo, rev = args
        except ValueError:
            self.parser.error('Missing arguments REPO and REV.')

        self.instancedir = os.path.abspath(os.path.join(repo, '../../'))

        admindir = os.path.join(self.instancedir, 'admin')
        reporoot = os.path.join(self.instancedir, 'repositories')

        self.log.debug('starting post-commit for %s (via %s)' %
                (self.instancedir, repo))

        self.run_script(
                os.path.join(self.instancedir, 'hooks', 'post-commit'),
                repo, rev)
        self.run_script(
                os.path.join(self.opts.datadir, 'hooks', 'post-commit'),
                repo, rev)

    def run_script(self, path, repo, rev):
        self.log.debug('checking for: %s' % path)
        if not os.access(path, os.X_OK):
            return

        self.log.info('running post-commit hook: %s' % path)
        rc = subprocess.call([path, repo, rev])
        self.log.debug('%s returned rc = %d' % (path, rc))

if __name__ == '__main__':
    Main().main()

