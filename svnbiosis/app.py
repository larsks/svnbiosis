#!/usr/bin/python

import os
import sys
import optparse
import logging
import ConfigParser

class App (object):

    def main(self):
        self.setup_basic_logging()
        parser = self.create_parser()

        opts, args = parser.parse_args()

        cfg = self.create_config()
        self.read_config(opts, cfg)
        self.setup_logging(opts, cfg)

        self.handle_args(parser, cfg, opts, args)

    def create_parser(self):
        parser = optparse.OptionParser()
        parser.add_option('--debug', action='store_true')
        parser.add_option('-f', '--config', metavar='FILE',
                default=os.path.expanduser('~/svntool.conf'))
        return parser

    def create_config(self):
        cfg = ConfigParser.ConfigParser()
        return cfg

    def read_config(self, opts, cfg):
        cfg.read(opts.config)

    def setup_basic_logging(self):
        logging.basicConfig()

    def setup_logging(self, opts, cfg):
        try:
            loglevel = cfg.get('svntool', 'loglevel')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            pass
        else:
            try:
                if opts.debug:
                    symbolic = logging.DEBUG
                else:
                    symbolic = logging._levelNames[loglevel]
            except KeyError:
                log.warning(
                    'Ignored invalid loglevel configuration: %r',
                    loglevel,
                    )
            else:
                logging.root.setLevel(symbolic)


    def handle_args(self, parser, cfg, opts, args):
        pass

