=========
SVNBIOSIS
=========

Svnbiosis (pronounced *svinbiosis*) is a gitosis-alike for Subversion
repositories.

Installation
============

To install from source, run::

  python setup.py install

Because Python's ``setuptools`` is horrid, you may also need to make sure the
``post-commit`` scripts are executable::

  chmod 755 .../site-packages/svnbiosis/resources/admin-post-commit
  chmod 755 .../site-packages/svnbiosis/resources/user-post-commit

Where ``...`` is the path to your Python library directory.

Usage
=====

Initialize a svnbiosis instance::

  svnbiosis-init -k /path/to/sshkey.pub username

Now you have a repository that is accessible via ``svn+ssh://`` using the
corresponding public key.  Alternatively, you could access the repository
as *username* via ``http://``, although note that these two mechanisms
require different sets of permissions and you may not be able to use both.

