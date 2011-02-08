import os
import sys

import app

class Main(app.App):
    def handle_args(self, parser, cfg, options, args):
        try:
            (user,) = args
        except ValueError:
            parser.error('Missing argument USER.')

        main_log = logging.getLogger('svntool.serve.main')
        os.umask(0022)

        os.chdir(os.path.expanduser('~'))

        os.execvp('svnserve', ['svnserve', '--config-file',
            'svnserve.conf', '-r', '.', '-t', '--tunnel-user', user])
        main_log.error('Cannot execute svnserve.')
        sys.exit(1)

