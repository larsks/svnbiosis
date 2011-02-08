#!/usr/bin/python

import os
import sys
import logging

import app

class Main(app.App):
    def handle_args(self, parser, cfg, options, args):
        try:
            repo, rev = args
        except ValueError:
            parser.error('Missing arguments REPO and REV.')

        main_log = logging.getLogger('svntool.postcommit.main')
        os.umask(0022)

        instancedir = os.path.abspath(os.path.join(repodir, '../../'))
        admindir = os.path.join(instancedir, 'admin')
        reporoot = os.path.join(instancedir, 'repositories')

        try:
            os.chdir(admindir)
        except OSError, detail:
            main_log.error('unable to access admin directory: %s' % detail)
            sys.exit(1)

        rc = subprocess.call(['svn', '--non-interactive', 'update', '-q'])

        authz = ConfigParser()
        authz.read('authz')

        for sec in authz.sections():
            if not ':' in sec:
                continue

            repo, path = sec.split(':')
            if not re_valid_repo.match(repo):
                continue

            repodir = os.path.join(reporoot, repo)
            if os.path.isdir(repodir):
                continue

            rc = subprocess.call(['svnadmin', 'create', repodir])


if __name__ == '__main__':
    x = Main()
    x.main()

