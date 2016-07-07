#!/usr/bin/env python

from setuptools import setup

setup(name='pymulti_change',
      version='0.8',
      description='A script to make mass changes to routers and switches.',
      author='James Williams',
      url='https://github.com/jtdub/pyMultiChange',
      dependency_links = ['https://github.com/jtdub/netlib/tarball/master#egg=netlib-0.0.7'],
      install_requires = ['netlib'],
      scripts=['bin/multi_change.py'])
