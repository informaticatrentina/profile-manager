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

'''
Fab file
========

This is used to deploy the application in testing and production

.. warning::

    TODO: Hanlde the custom configuration on the destination machine

'''


from fabric.api import env, execute, local, put, run, sudo
from os.path import exists

from fabric.utils import warn


# the user to use for the remote commands
# env.user = 'www-data'
deploy_user = 'www-data'

# the servers where the commands are executed
env.hosts = ['hubx.ahref.eu', 'huby.ahref.eu']
env.hosts = ['huby.ahref.eu', ]

# this path is hardcoded
DEST_VE = "/srv/www/profile_manager/ve"


DEST_PYTHON = "%s/bin/python" % DEST_VE
DEST_PIP = "%s/bin/pip" % DEST_VE


def _get_dist():
    """Return local dist name (Package-Version)"""
    dist = local('python setup.py --fullname', capture=True).strip()
    return dist


def build():
    """Build a new source distribution as tarball"""
    dist = _get_dist()
    if not exists('dist/%s.tar.gz' % dist):
        local('python setup.py sdist --formats=gztar', capture=False)
    else:
        warn("Dist %s already exsist!" % dist)


def _deploy():
    """Deploys the package on the server"""
    dist = _get_dist()
    # upload the source tarball to the temporary folder on the server
    dist_remote = '/var/tmp/%s.tar.gz' % dist
    put('dist/%s.tar.gz' % dist, dist_remote)
    # now install the package with our virtual environment's python
    # interpreter
    sudo('%s install %s' % (DEST_PIP, dist_remote), user=deploy_user)
    # now that all is set up, delete the folder again
    run('rm -f %s' % dist_remote)
    # brute force wsgi restart
    # TODO: use touch-reload
    sudo('/etc/init.d/uwsgi restart', user="root")


def deploy():
    """Build and Deploy the package on the server"""
    execute(pack)
    execute(_deploy)
