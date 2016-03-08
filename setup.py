#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='qiniu-sync',
      version='1.0',
      description='Sync local file to Qiniu',
      author='Robert Lu',
      author_email='robberphex@gmail.com',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      entry_points={
          'console_scripts': [
              'qiniu-sync = qiniu_sync:main'
          ]
      },
      )
