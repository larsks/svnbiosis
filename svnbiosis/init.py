#!/usr/bin/python

import os

if not hasattr(os.path, 'relpath'):
    import stupid
    os.path.relpath = stupid.relpath

import sys
import logging
import subprocess
import glob

from distutils.dir_util import copy_tree
from distutils.file_util import copy_file

import resources
import app
import ssh
import svn

authz_template='''# Allow access for primary user.
[admin:/]
%(user)s = rw
'''

class Main(app.App):
    logtag = 'svnbiosis.init'

    def create_parser(self):
        parser = super(Main, self).create_parser()
        parser.add_option('-k', '--key')

        return parser

    def handle_args(self, args):
        try:
            (user,) = args
        except ValueError:
            self.parser.error('Missing argument USER.')

        self.log.debug('running init for user: %s' % user)

        if self.opts.key and not os.path.isfile(self.opts.key):
            self.log.error('cannot access public key "%s".' % self.opts.key)
            sys.exit(1)

        try:
            os.chdir(self.opts.instancedir)
        except OSError, detail:
            self.log.error('unable to access instance directory: %s' % detail)
            sys.exit(1)

        self.log.info('creating admin repository')
        os.mkdir('repositories')

        repo = svn.createRepository(
                os.path.join('repositories', 'admin'),
                hooks = {
                    'post-commit':
                    os.path.join(self.resourcedir, 'post-commit')
                    },
                conf = {
                    'authz':
                    os.path.relpath(
                        os.path.join('admin', 'authz'),
                        os.path.join('repositories', 'admin', 'conf')
                        ),
                    'svnserve.conf':
                    os.path.join(self.resourcedir, 'svnserve.conf'),
                    }
                )

        repo.checkout()
        self.setup_repository(user)
        self.install_template()
        repo.add(glob.glob('admin/*'))
        repo.commit('initial commit')

    def install_resource(self, src, target):
        copy_file(
                os.path.join(self.resourcedir, src),
                target)

    def setup_repository(self, user):
        self.setup_keys(user)

        authz = os.path.join(self.opts.instancedir, 'admin', 'authz')
        self.install_resource('authz', authz)

        fd = open(authz, 'a')
        print >>fd, authz_template % dict(user = user)
        fd.close()

        self.install_resource('svnbiosis.conf',
                os.path.join(self.opts.instancedir, 'admin'))

    def setup_keys(self, user):
        keydir = os.path.join('admin', 'keydir')
        os.mkdir(keydir)
        if self.opts.key:
            copy_file(self.opts.key,
                    os.path.join(keydir, '%s.pub' % user))

    def install_template(self):
        templatedir = os.path.join(self.opts.datadir, 'template')
        if os.path.isdir(templatedir):
            self.log.info('populating admin repository from template')
            copy_tree(
                    templatedir, 'admin', verbose=True)

if __name__ == '__main__':
    Main().main()

