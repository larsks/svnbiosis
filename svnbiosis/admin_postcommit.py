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

re_valid_repo = re.compile('^[\w\d.-]+$')

class Main(app.App):
    logtag = 'svnbiosis.admin-post-commit'

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

        if not os.path.isdir(admindir):
            self.log.error('unable to access admin directory (%s).' %
                    admindir)
            sys.exit(1)

        self.log.debug('updating active configuration from repository')
        admin = svn.Repository(
                os.path.join(reporoot, 'admin'),
                admindir)
        admin.update()

        self.create_repositories()
        self.update_keys()

    def update_keys(self):
        sshdir = os.path.join(self.instancedir, '.ssh')

        if not os.path.isdir(sshdir):
            self.log.debug('creating .ssh directory')
            os.mkdir(sshdir)

        self.log.debug('rewriting authorized_keys file')
        ssh.writeAuthorizedKeys(
                os.path.join(sshdir, 'authorized_keys'),
                os.path.join(self.instancedir, 'admin', 'keydir'))

    def create_repositories(self):
        self.log.debug('looking for new repositories')

        authz = ConfigParser.ConfigParser()
        authz.read(os.path.join(self.instancedir, 'admin', 'authz'))

        for sec in authz.sections():
            if not ':' in sec:
                continue

            reponame, path = sec.split(':')
            if not re_valid_repo.match(reponame):
                self.log.warning('invalid repo name: %s' % reponame)
                continue

            repodir = os.path.join(self.instancedir, 'repositories', reponame)
            if os.path.isdir(repodir):
                continue

            self.log.info('creating new repository %s (%s)' % (reponame, repodir))
            repo = svn.createRepository(repodir,
                    conf = {
                        'authz':
                        os.path.relpath(
                            os.path.join(self.instancedir, 'admin', 'authz'),
                            os.path.join(repodir, 'conf')
                            ),
                        'svnserve.conf':
                        os.path.join(self.resourcedir, 'svnserve.conf'),
                        },
                    hooks = {
                        'post-commit':
                        os.path.join(self.resourcedir, 'user-post-commit')
                        'pre-revprop-change':
                        os.path.join(self.resourcedir, 'user-pre-revprop-change')
                        },
                    )


if __name__ == '__main__':
    Main().main()

