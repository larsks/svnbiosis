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
import hookscript

re_valid_repo = re.compile('^[\w\d]+$')

class Main(hookscript.Main):
    logtag = 'svnbiosis.post-commit-user'

    def handle_args(self, args):
        try:
            repo, rev, user, propname, changetype = args
        except ValueError:
            self.parser.error('Expecting REPO REV USER PROPNAME CHANGETYPE.')

        self.opts.instancedir = os.path.abspath(os.path.join(repo, '../../'))

        admindir = os.path.join(self.opts.instancedir, 'admin')
        reporoot = os.path.join(self.opts.instancedir, 'repositories')

        self.log.debug('starting pre-revprop-change for %s (via %s)' %
                (self.opts.instancedir, repo))

        if self.cfg.get('svnbiosis', 'allow_revprop_change') == 'YES':
            sys.exit(0)
        else:
            print >>sys.stderr, 'Revision property changes are currently disabled.'
            print >>sys.stderr, 'Set allow_revprop_change=YES in svnbiosis.conf to enable.'
            sys.exit(1)

    def create_config(self):
        cfg = super(Main, self).create_config()
        cfg.set('DEFAULT', 'allow_revprop_change', 'NO')
        return cfg

if __name__ == '__main__':
    Main().main()

