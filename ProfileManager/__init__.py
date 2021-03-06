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
ProfileManager
==============

TODO: replace this line with proper project description.
'''

import pkg_resources
pkg_resources.declare_namespace(__name__)


# The __init__.py must contain the app
# http://flask.pocoo.org/docs/patterns/packages/
# but the __init__.py is run by setup.py
# http://stackoverflow.com/questions/12383246/why-does-setup-py-runs-the-package-init-py # NOQA
# so, this is a workaround to handle both
try:
    from flask import Flask
except ImportError:  # pragma: no cover
    import sys
    sys.exit("You should not reach this point")


from flask.ext.bootstrap import Bootstrap
from flask.ext.babelex import Babel

from flask.ext.uploads import configure_uploads, UploadSet, IMAGES

from flask.ext.principal import Principal

images = UploadSet("images", IMAGES)

from ProfileManager.blueprints.user import user

from ProfileManager.blueprints.auth.auth import auth
from ProfileManager.blueprints.auth.auth import login_manager


def config_app(app):
    # Load setting using various methods
    # TODO: do relative o package import
    app.config.from_object('ProfileManager.defaults_settings')
    # TODO: document the PM_SETTINGS
    app.config.from_envvar('PM_SETTINGS', silent=True)


app = Flask(__name__)

config_app(app)
babel = Babel(app)
Bootstrap(app)

configure_uploads(app, (images, ))
app.register_blueprint(user, url_prefix='')
app.register_blueprint(auth, url_prefix='/auth')

Principal(app)

login_manager.init_app(app)
