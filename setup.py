# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 <ahref Foundation -- All rights reserved.
# Author: Daniele Pizzolli <daniele@ahref.eu>
#
# This file is part of the ProfileManager project.
#
# This file can not be copied and/or distributed without the express
# permission of <ahref Foundation.
#
###############################################################################


from setuptools import setup

with open('requirements/base.txt') as f:
    requirements_base = f.read().splitlines()

with open('requirements/test.txt') as f:
    requirements_test = f.read().splitlines()

with open('requirements/dependencies.txt') as f:
    dependencies = f.read().splitlines()

setup(
    name='ProfileManager',
    version=open('version.txt').read().strip(),
    author = 'Daniele Pizzolli',
    author_email='daniele@ahref.eu',
    packages=['ProfileManager', 'ProfileManager.test', 'ProfileManager.blueprints'],
    # namespace_packages=['ProfileManager'],
    keywords = 'ProfileManager',
    url='http://gitlab.ahref.eu/aggregator/ProfileManager.git',
    license='Proprietary License',
    long_description=open('README.rst').read(),
    description = ('ProfileManager is the frontend for the profile users'),
    entry_points='''
        [console_scripts]
        pm = ProfileManager.manage:main
        ''',
    # To skip problems of local eggs we make fat requirements:
    # http://stackoverflow.com/questions/1843424/setup-py-test-egg-install-location
    install_requires=requirements_base + requirements_test,
    dependency_links=dependencies,
    include_package_data=True,
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
