#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='qiniu-up',
      version='0.2.0',
      description='Sync local file to Qiniu',
      author='Robert Lu',
      author_email='robberphex@gmail.com',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[
          "requests",
          "qiniu > 7.0.6"
      ],
      entry_points={
          'console_scripts': [
              'qiniu-up = qiniu_up:main'
          ]
      },
      )
