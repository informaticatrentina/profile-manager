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
User Login Blueprint
====================

TODO: replace this line with proper project description.
'''

import urllib

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for
    )

from flask.ext.login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    )

from flask.ext.wtf import Form
from wtforms import  TextField, PasswordField

from flask.ext.principal import (
    AnonymousIdentity,
    Identity,
    identity_changed,
    )

from flask.ext.babelex import lazy_gettext as _

import requests as requestclient


auth = Blueprint('auth', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/auth_static'  # TODO: be more modular
                 )

login_manager = LoginManager()

from flask.ext.login import UserMixin


class User(UserMixin):
    id = None
    email = None
    password = None
    first_name = None
    last_name = None
    sex = None


# TODO: this is the same of user.py!
# move to a module!
def _get_user(userid):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s%s' % (
        current_app.config['IM_URL'],
        '/users/',
        userid
        )
    rc = requestclient.get(endpoint, auth=auth)
    user = rc.json()
    appuser = User()
    appuser.id = user['_id']
    appuser.email = user['email']
    appuser.first_name = user['firstname']
    appuser.last_name = user['lastname']
    if 'sex' in user.keys():
        appuser.sex = user['sex'][0]
    return appuser


def _check_login(useremail, password):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    encoded_useremail = urllib.quote_plus(useremail)
    encoded_password = urllib.quote_plus(password)
    endpoint = '%s%s/?where={"email": "%s", "password": "%s"}' % (
        current_app.config['IM_URL'],
        '/users',
        encoded_useremail,
        encoded_password
        )
    rc = requestclient.get(endpoint, auth=auth)
    user = rc.json()
    if len(user['_items']) == 1:
        appuser = User()
        appuser.id = user['_items'][0]['_id']
        appuser.email = user['_items'][0]['email']
        return appuser
    else:
        from flask import flash
        flash('Either email or password is wrong', 'error')
        return None


@login_manager.user_loader
def load_user(userid):
    return _get_user(userid) or None


class LoginForm(Form):
    email = TextField(description=_("Email"))
    password = PasswordField(description=_("Password"))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Show a page with a form for user login

    :query string next: the url to redirect after logout (optional)

    If there is no `next` param the user will be redirected to:
    :http:get:`/edit/<userid>` page.

    .. note::

        The link to the edit page does not work to sphinx limitgation.
    """

    if current_user.is_authenticated():
        return redirect(request.args.get('next') or url_for('user.edit', userid=current_user.id))

    # A hypothetical login form that uses Flask-WTF
    form = LoginForm(request.form)

    # Validate form input
    if form.validate_on_submit():
        # Retrieve the user from the hypothetical datastore
        # Compare passwords (use password hashing production)
        user = _check_login(form.email.data, form.password.data)
        if user:
            # Keep the user info in the session using Flask-Login
            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(user.id))

            return redirect(
                request.args.get('next') or
                url_for('user.edit', userid=user.id))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Logout the user and redirect to the home or to the

    :query string next: the url to redirect after logout (optional)
    """

    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')
