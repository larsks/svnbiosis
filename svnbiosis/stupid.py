#!/usr/bin/python

import os
from os.path import abspath, sep, commonprefix, pardir, curdir, join

'''This module takes care of some of the stupid that comes with the older
version of Python available on RHEL5 and derivatives.'''

def relpath(path, start=curdir):
    """Return a relative version of a path (from posixpath.py)"""

    if not path:
        raise ValueError("no path specified")

    start_list = abspath(start).split(sep)
    path_list = abspath(path).split(sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(commonprefix([start_list, path_list]))

    rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return join(*rel_list)

