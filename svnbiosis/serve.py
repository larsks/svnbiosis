import os
import sys
import logging

import app

class Main(app.App):
    logtag = 'svnbiosis.serve'

    def handle_args(self, args):
        try:
            (user,) = args
        except ValueError:
            self.parser.error('Missing argument USER.')

        os.chdir(self.opts.instancedir)

        self.log.info('starting server for user: %s' % user)
        os.execvp('svnserve', ['svnserve', 
            '-r', 'repositories',
            '-t', '--tunnel-user', user])

        self.log.error('Cannot execute svnserve.')
        sys.exit(1)

if __name__ == '__main__':
    Main().main()

