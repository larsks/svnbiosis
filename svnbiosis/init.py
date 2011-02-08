#!/usr/bin/python

import os
import sys
import logging
import subprocess
import glob

from distutils.dir_util import copy_tree
from distutils.file_util import copy_file

import app
import ssh

authz_template='''
[admin:/]
%(user)s = rw
'''

postcommit_template='''#!/bin/sh
python -m svnbiosis.postcommit "$@"
'''

class Main(app.App):
    def create_parser(self):
        parser = super(Main, self).create_parser()
        parser.add_option('-k', '--key')

        return parser

    def handle_args(self, args):
        try:
            (user,) = args
        except ValueError:
            self.parser.error('Missing argument USER.')

        main_log = logging.getLogger('svnbiosis.init.main')
        os.umask(0022)

        if self.opts.key and not os.path.isfile(self.opts.key):
            main_log.error('cannot access public key "%s".' % self.opts.key)
            sys.exit(1)

        try:
            os.chdir(self.opts.instancedir)
        except OSError, detail:
            main_log.error('unable to access instance directory: %s' % detail)
            sys.exit(1)

        main_log.info('creating admin repository')
        os.mkdir('repositories')

        adminrepo = os.path.join('repositories', 'admin')
        postcommit_hook = os.path.join(adminrepo, 'hooks', 'post-commit')

        rc = subprocess.call(['svnadmin', 'create', adminrepo])
        fd = open(postcommit_hook, 'w')
        print >>fd, postcommit_template
        fd.close()
        os.chmod(postcommit_hook, 0755)

        rc = subprocess.call(['svn', 'co', 
            'file://%s/repositories/admin' % self.opts.instancedir,
            'admin'])

        main_log.info('populating admin repository')
        copy_tree(
                os.path.join(self.opts.datadir, 'template'),
                'admin',
                verbose=True)

        keydir = os.path.join('admin', 'keydir')
        os.mkdir(keydir)

        if self.opts.key:
            copy_file(self.opts.key, os.path.join(keydir, '%s.pub' % user))

        authz = os.path.join('admin', 'authz')
        fd = open(authz, 'a')
        print >>fd, authz_template % dict(user = user)
        fd.close()

        rc = subprocess.call(['svn', 'add'] + glob.glob('admin/*'))
        rc = subprocess.call(['svn', 'commit', '-m', 'initial commit',
            'admin'])

if __name__ == '__main__':
    Main().main()

