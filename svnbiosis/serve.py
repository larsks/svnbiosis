import os
import sys

import app

class Main(app.App):
    def handle_args(self, args):
        try:
            (user,) = args
        except ValueError:
            parser.error('Missing argument USER.')

        main_log = logging.getLogger('svnbiosis.serve.main')
        os.umask(0022)

        os.chdir(self.opts.instancedir)

        os.execvp('svnserve', ['svnserve', '--config-file',
            'svnserve.conf', '-r', '.', '-t', '--tunnel-user', user])
        main_log.error('Cannot execute svnserve.')
        sys.exit(1)

if __name__ == '__main__':
    Main().main()

