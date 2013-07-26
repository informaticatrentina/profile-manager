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


from flask import Blueprint, render_template


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
    return render_template('user_show.html')


@user.route('/edit/<userid>')
def edit(userid):
    return render_template('user_edit.html')
