=========
SVNBIOSIS
=========

Svnbiosis (pronounced *svinbiosis*) is a gitosis-alike for Subversion repositories.

Installation
============

To install from source, run::

  python setup.py install

Because Python's ``setuptools`` is horrid, you may also need to make sure the
``post-commit`` script is executable::

  chmod 755 .../site-packages/svnbiosis/resources/post-commit

Where ``...`` is the path to your Python library directory.

Usage
=====

Initialize a svnbiosis instance::

  svnbiosis-init -k /path/to/sshkey.pub username

Now you have a repository that is accessible via `svn+ssh://` using the
corresponding public key (and by user *username* if you have set up Apache
to serve out your repositories).

