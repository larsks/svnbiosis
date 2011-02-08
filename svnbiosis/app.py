#!/usr/bin/python

import os
import sys
import optparse
import logging
import ConfigParser

import resources

class App (object):
    logtag = 'svnbiosis.unknown.unknown'

    def run(class_):
        app = class_()
        return app.main()
    run = classmethod(run)

    def main(self):
        self.setup_basic_logging()

        parser = self.create_parser()
        opts, args = parser.parse_args()
        cfg = self.create_config()

        self.opts = opts
        self.cfg = cfg
        self.parser = parser
        self.resourcedir = os.path.dirname(resources.__file__)

        self.fixup_paths()
        self.read_config()
        self.setup_logging()
        self.setup_umask()

        self.log.debug('finished generic setup')

        self.handle_args(args)

    def fixup_paths(self):
        self.opts.instancedir = os.path.abspath(self.opts.instancedir)
        self.opts.datadir = os.path.abspath(self.opts.datadir)
        self.resourcedir = os.path.abspath(self.resourcedir)

    def setup_umask(self):
        try:
            umask = int(self.cfg.get('svnbiosis', 'umask'), 8)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            umask = 0022

        self.log.debug('set umask to %04o.' % umask)
        os.umask(umask)


    def create_parser(self):
        parser = optparse.OptionParser()
        parser.add_option('--debug', action='store_true')
        parser.add_option('-d', '--instancedir',
                default=os.environ.get('SVNBIOSIS_INSTANCE',
                    os.environ.get('HOME', os.path.expanduser('~'))))
        parser.add_option('-D', '--datadir',
                default=os.environ.get('SVNBIOSIS_DATADIR',
                    '/usr/share/svnbiosis'))
        return parser

    def create_config(self):
        cfg = ConfigParser.ConfigParser()
        return cfg

    def read_config(self):
        cfgpath = os.path.join(self.opts.instancedir, 'admin',
                'svnbiosis.conf')
        self.cfg.read(cfgpath)

    def setup_basic_logging(self):
        logging.basicConfig()

    def setup_logging(self):
        try:
            if self.opts.debug:
                loglevel = 'DEBUG'
            else:
                loglevel = self.cfg.get('svnbiosis', 'loglevel')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            pass
        else:
            try:
                symbolic = logging._levelNames[loglevel]
            except KeyError:
                log.warning(
                    'Ignored invalid loglevel configuration: %r',
                    loglevel,
                    )
            else:
                logging.root.setLevel(symbolic)

        self.log = logging.getLogger(self.logtag)

    def handle_args(self, args):
        pass

