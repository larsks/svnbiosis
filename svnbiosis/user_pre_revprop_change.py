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
            repo, rev, user, propname, changetype = args
        except ValueError:
            self.parser.error('Expecting REPO REV USER PROPNAME CHANGETYPE.')

        self.instancedir = os.path.abspath(os.path.join(repo, '../../'))

        admindir = os.path.join(self.instancedir, 'admin')
        reporoot = os.path.join(self.instancedir, 'repositories')

        self.log.debug('starting pre-revprop-change for %s (via %s)' %
                (self.instancedir, repo))

        if self.cfg.get('svnbiosis', 'allow_revprop_change') == 'YES':
            sys.exit(0)
        else:
            sys.exit(1)

    def create_config(self):
        cfg = super(app.app, self).create_config()
        cfg.set('DEFAULT', 'allow_revprop_change', 'NO')
        return cfg

if __name__ == '__main__':
    Main().main()

