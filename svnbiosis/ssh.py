#!/usr/bin/python

import os
import sys
import fnmatch
import shlex
import re
import tempfile

re_valid_user = re.compile(r'^[a-zA-Z][a-zA-Z0-9_.-]*(@[a-zA-Z][a-zA-Z0-9.-]*)?$')
authorized_keys_template = ('command="svntool-serve %(user)s",no-port-forwarding,'
              +'no-X11-forwarding,no-agent-forwarding,no-pty %(keytype)s '
              +'%(keydata)s SVNTOOL:%(user)s')

def isSafeUsername(user):
    match = re_valid_user.match(user)
    return (match is not None)

def readKeys(keydir):
    for filename in fnmatch.filter(os.listdir(keydir), '*.pub'):
        basename, ext = os.path.splitext(filename)

        if not isSafeUsername(basename):
            continue

        user = basename

        filepath = os.path.join(keydir, filename)
        fd = open(filepath)
        for line in fd:
            if line.startswith('#'):
                continue
            if not line.strip():
                continue

            parts = shlex.split(line)
            if parts[0].startswith('ssh-'):
                keytype = parts[0]
                keydata = parts[1]
            elif parts[1].startswith('ssh-'):
                keytype = parts[1]
                keydata = parts[2]
            else:
                continue

            yield((user, keytype, keydata))

def generateAuthorizedKeys(keys):
    for (user, keytype, keydata) in keys:
        yield authorized_keys_template % dict(
                user=user,
                keytype=keytype,
                keydata=keydata)

def filterAuthorizedKeys(fd):
    for line in fd:
        line = line.strip()

        if shlex.split(line)[-1].startswith('SVNTOOL:'):
            continue
        else:
            yield(line)

def writeAuthorizedKeys(path, keydir):
    tmp = tempfile.NamedTemporaryFile(delete=False,
            dir=os.path.dirname(path))

    try:
        infd = open(path)
    except IOError, detail:
        if detail.errno == errno.ENOENT:
            infd = None
        else:
            raise

    try:
        try:
            if infd is not None:
                for line in filterAuthorizedKeys(infd):
                    print >>tmp, line

            keygen = readKeys(keydir)
            for line in generateAuthorizedKeys(keygen):
                print >>tmp, line
        finally:
            tmp.close()
    finally:
        if infd is not None:
            infd.close()
    os.rename(tmp.name, path)


if __name__ == '__main__':
    keys = readKeys(sys.argv[1])
    writeAuthorizedKeys(sys.argv[1], sys.argv[2])

