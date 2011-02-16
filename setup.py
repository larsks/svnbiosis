#!/usr/bin/python

from setuptools import setup, find_packages
import os

setup(
    name = "svnbiosis",
    version = "1",
    packages = find_packages(),

    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@seas.harvard.edu',
    description = 'software for hosting Subversion repositories',
    long_description = open('README.rst', 'r').read(),
    license = 'BSD',
    keywords = 'svn subversion scm version-control ssh',

    entry_points = {
        'console_scripts': [
            'svnbiosis-serve = svnbiosis.serve:Main.run',
            'svnbiosis-admin-post-commit = svnbiosis.admin_postcommit:Main.run',
            'svnbiosis-user-post-commit = svnbiosis.user_postcommit:Main.run',
            'svnbiosis-init = svnbiosis.init:Main.run',
            ],
        },

    package_data={
        'svnbiosis.resources': ['*']
        },

    # templates need to be a real directory, for git init
    zip_safe=False,

    install_requires=[
        # setuptools 0.6a9 will have a non-executeable post-update
        # hook, this will make gitosis-admin settings not update
        # (fixed in 0.6c5, maybe earlier)
        'setuptools>=0.6c5',
        ],
    )

