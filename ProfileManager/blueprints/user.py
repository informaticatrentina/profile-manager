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
User Blueprint
==============

TODO: replace this line with proper project description.
'''

from flask import Blueprint, render_template, redirect, request, url_for

from flask.ext.babelex import lazy_gettext as _

from ProfileManager.blueprints.form import UserProfileForm


user = Blueprint('user', __name__,
                 template_folder='user/templates',
                 static_folder='user/static',
                 static_url_path='/user_static'  # TODO: be more modular
                 )


@user.route('/')
def home():
    return render_template('user_home.html')


@user.route('/<userid>')
def show(userid):
    user = {}
    return render_template('user_show.html', user=user)


@user.route('/edit/<userid>', methods=['GET', 'POST'])
def edit(userid):
    # TODO: add default user data
    form = UserProfileForm(request.form, obj={})
    if request.method == 'POST' and form.validate():
        pass
        # TODO: flash('Thanks for registering')
        return redirect(url_for('/'))  # TODO view
    return render_template(
        'user_edit.html',
        form=form,
        title=_(u"Edit your profile"))
