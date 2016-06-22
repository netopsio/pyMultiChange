#!/usr/bin/env python

from setuptools import setup

setup(name='pymulti_change',
      version='0.7',
      description='A script to make mass changes to routers and switches.',
      author='James Williams',
      url='https://github.com/jtdub/pyMultiChange',
      dependency_links = ['http://github.com/jtdub/netlib/tarball/master'],
      install_requires = ['netlib'],
      scripts=['bin/multi_change.py'])
