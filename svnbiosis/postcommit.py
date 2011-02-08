#!/usr/bin/python

import os
import sys
import logging
import subprocess
import ConfigParser
import re

import app
import ssh

re_valid_repo = re.compile('^[\w\d]+$')

class Main(app.App):
    logtag = 'svnbiosis.post-commit'

    def handle_args(self, args):
        try:
            repo, rev = args
        except ValueError:
            self.parser.error('Missing arguments REPO and REV.')

        instancedir = os.path.abspath(os.path.join(repo, '../../'))
        admindir = os.path.join(instancedir, 'admin')
        reporoot = os.path.join(instancedir, 'repositories')

        self.log.debug('starting post-commit for %s (via %s)' %
                (instancedir, repo))

        try:
            os.chdir(admindir)
        except OSError, detail:
            self.log.error('unable to access admin directory: %s' % detail)
            sys.exit(1)

        self.log.debug('updating active configuration from repository')
        rc = subprocess.call(['svn', '--non-interactive', 'update', '-q'])

        self.log.debug('looking for new repositories')
        authz = ConfigParser.ConfigParser()
        authz.read('authz')

        for sec in authz.sections():
            if not ':' in sec:
                continue

            repo, path = sec.split(':')
            if not re_valid_repo.match(repo):
                self.log.warning('invalid repo name: %s' % repo)
                continue

            repodir = os.path.join(reporoot, repo)
            if os.path.isdir(repodir):
                continue

            self.log.info('creating new repository %s (%s)' % (repo, repodir))
            rc = subprocess.call(['svnadmin', 'create', repodir])

        sshdir = os.path.join(instancedir, '.ssh')

        if not os.path.isdir(sshdir):
            os.mkdir(sshdir)

        self.log.debug('rewriting authorized_keys file')
        ssh.writeAuthorizedKeys(
                os.path.join(sshdir, 'authorized_keys'),
                os.path.join(admindir, 'keydir'))

if __name__ == '__main__':
    Main().main()

