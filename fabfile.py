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


from fabric.api import env, execute, local, prefix, put, run, sudo, cd, settings
from os.path import exists

from fabric.utils import warn


# Use posix shell
env.shell = "/bin/sh -c"

env.roledefs = {
    'dev': ['hubx.ahref.eu'],
    'production': ['huby.ahref.eu']
}

# this path is hardcoded
R_HOME = "/srv/www/profile_manager/"
DEST_VE = "/srv/www/profile_manager/ve"

BIN_ACTIVATE = "{}/bin/activate".format(DEST_VE)

# gid
R_UID = "403"
R_GID = "403"

# remote use name
# R_USER = "profilemanager"  # This is for dev
R_USER = "www-data"  # TODO: create separate user user for production


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
    sudo('%s install %s' % (DEST_PIP, dist_remote), user=R_USER)
    # now that all is set up, delete the folder again
    run('rm -f %s' % dist_remote)
    # brute force wsgi restart
    # TODO: use touch-reload
    sudo('/etc/init.d/uwsgi restart', user="root")


def init_packages():
    """Install required packages"""
    # TODO
    pass


def init_user():
    """Create the user"""
    sudo("addgroup --system --gid {R_GID} {R_USER}".format(R_GID=R_GID,
                                                           R_USER=R_USER))
    sudo("adduser --system --home {R_HOME}"
         " --uid {R_UID} --gid {R_GID}"
         " --disabled-password {R_USER}".format(
             R_HOME=R_HOME, R_UID=R_UID, R_GID=R_GID, R_USER=R_USER))


def init_ve():
    """Create the ve"""
    with settings(sudo_user=R_USER):
        with cd(R_HOME):  # what happens if we can not cd here?
            sudo('virtualenv ve')


def init_uwsgi():
    """Create the uwsgi conf file"""
    # TODO: the ini file is harcoded. Use jinia from contrib
    put('provisioning/etc/uwsgi/apps-available/profile-manager.ini',
        '/etc/uwsgi/apps-available/profile-manager.ini',
        use_sudo=True)
    with cd('/etc/uwsgi/apps-enabled'):
        sudo('ln -s ../apps-available/profile-manager.ini .')


def init_nginx():
    """Create the nginx conf file"""
    # TODO: the ini file is harcoded. Use jinia from contrib
    put('provisioning/etc/nginx/sites-available/profile-manager',
        '/etc/nginx/sites-available/profile-manager',
        use_sudo=True)
    with cd('/etc/nginx/sites-enabled'):
        sudo('rm profile-manager')
        sudo('ln -s ../sites-available/profile-manager .')
    sudo('/etc/init.d/nginx restart', user="root")


def init_settings():
    pass


def deploy():
    """Build and Deploy the package on the server"""
    execute(build)
    execute(_deploy)

def get_remote_version():
    """Print the remote version"""
    # With a trick to enable the virtualenv with sudo...
    # Hopefully one day fab will support with sudo(), virtualenv()
    with cd(R_HOME), prefix('. {}'.format(BIN_ACTIVATE)):
        sudo('pip freeze | grep ProfileManager', user=R_USER)

