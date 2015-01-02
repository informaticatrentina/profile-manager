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


# WARNNG: must be changed to False in production!
DEBUG = True

# WARNNG: must be changed in production!
SECRET_KEY = "e&+aq@nfo_%p@=9l#7=(-9675+*!+gt0-&8gt)^9=uws42a5oc"

# Do not user google cdn
BOOTSTRAP_USE_CDN = False

# Use the font awesome
BOOTSTRAP_FONTAWESOME = True

# TODO: with BOOTSTRAP serve the local jquery and do not rely on the google cdn

# Force locale to italian
BABEL_DEFAULT_LOCALE = 'it'

# IM_URL
IM_URL = "http://localhost:8001/v1"
IM_USER = "yaiT6eequi7faig7aeSh0phi9id3iu3B"
IM_PASSWORD = ""

# Set the upload folder, change in production to a suitable storage dir!
UPLOAD_FOLDER = '/vat/tmp'

# Settings for flask-upload
# Set the upload folder, change in production to a suitable storage dir!
UPLOADS_DEFAULT_DEST = '/var/tmp'

UPLOADS_DEFAULT_URL = 'files'

# Enable wtf 18n

WTF_I18N_ENABLED = True

# Remote Eve version
# Use '0.0.6' for production until version 0.0.7 of the identity manager
# Use '0.0.8' for development
REMOTE_EVE_VERSION = '0.2.0'
