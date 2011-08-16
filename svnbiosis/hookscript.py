#!/usr/bin/python

import os

import app

class Main(app.App):
    def parse_args(self):
        opts, args = super(Main, self).parse_args()

        try:
            repo = args[0]
        except IndexError:
            self.parser.error('Missing arguments REPO.')

        self.opts.instancedir = os.path.abspath(os.path.join(repo, '../../'))

        return opts, args

if __name__ == '__main__':
    Main().main()

