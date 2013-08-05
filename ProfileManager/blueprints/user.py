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

import requests as requestclient

from time import time

from flask import (
    Blueprint, current_app, render_template, redirect, request, url_for
)

from flask.ext.babelex import lazy_gettext as _

from ProfileManager.blueprints.form import UserProfileForm


user = Blueprint('user', __name__,
                 template_folder='user/templates',
                 static_folder='user/static',
                 static_url_path='/user_static'  # TODO: be more modular
                 )

# TODO: how can we import the set from the current_app
from flask.ext.uploads import UploadSet, IMAGES

images = UploadSet("images", IMAGES)


def parse_page(links):
    """Parse links from eve for easy pagination"""

    from urlparse import urlparse as up, parse_qs

    for i in ('first', 'last', 'next', 'prev'):
        links.setdefault(i, {'href': '='})

    first = parse_qs(up(links['first']['href']).query).get('page', (0, ))[0]
    last = parse_qs(up(links['last']['href']).query).get('page', (0, ))[0]
    next = parse_qs(up(links['next']['href']).query).get('page', (0, ))[0]
    prev = parse_qs(up(links['prev']['href']).query).get('page', (0, ))[0]

    page = dict(
        first=first,
        last=last,
        next=next,
        prev=prev,
    )

    return page


def _get_user(userid):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s%s' % (
        current_app.config['IM_URL'],
        '/users/',
        userid
        )

    rc = requestclient.get(endpoint, auth=auth)
    user = rc.json()

    return user


def _generate_and_save_thumbnail(origin, destination, h, w):
    from PIL import Image
    image = Image.open(origin)
    image = image.resize((w, h), Image.ANTIALIAS)
    image.save(destination)


@user.route('/')
def home():
    return redirect(url_for('.index'))


@user.route('/index/', defaults={'page': 1})
@user.route('/index/<int:page>')
def index(page):

    start = time()
    users = list()
    pages = list()

    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s%s' % (
        current_app.config['IM_URL'],
        '/users/?max_results=20&page=',
        page)

    rc = requestclient.get(endpoint, auth=auth)
    data = rc.json()

    if '_items' in data:
        users = data['_items']

    if '_links' in data:
        pages = parse_page(data['_links'])

    timetorender = (time() - start) * 1000

    return render_template(
        'user_home.html',
        users=users,
        timetorender=timetorender,
        pages=pages)


@user.route('/show/<userid>')
def show(userid):
    user = _get_user(userid)

    if '_links' in user:
        del(user['_links'])

    return render_template('user_show.html', user=user)


@user.route('/edit/<userid>', methods=['GET', 'POST'])
def edit(userid):
    user = _get_user(userid)

    form = UserProfileForm(request.form, obj=user)

    if request.method == 'POST' and form.validate():
        # Handle the photo upload
        name_upload = request.files.get('photo').filename
        extension = os.path.splitext(name_upload)[1]
        name_original = "{}_original{}".format(userid, extension)
        name_resize = "{}.{}".format(userid, 'jpg')
        filename = images.save(request.files.get('photo'), name=name_original)

        _generate_and_save_thumbnail(
            images.path(filename),
            images.path(name_resize),
            370,
            370,
        )
        # TODO: put the data back to the im
        return redirect(url_for('/'))  # TODO view

    if '_links' in user:
        del(user['_links'])

    return render_template(
        'user_edit.html',
        form=form,
        user=user,
        title=_(u"Edit your profile"))


@user.route('/photo/<userid>/<size>/', defaults={'size': 1})
def photo(userid, size):
    """Return the user photo or the default one"""
    # TODO: implement resize!

    from os.path import basename, dirname, exists

    from flask import send_from_directory

    name_resize = "{}.{}".format(userid, 'jpg')

    file_path = images.path(name_resize)
    if not exists(file_path):
        # Return the default
        from pkg_resources import resource_filename
        resource_name = 'blueprints/user/static/img/foto_anonima.jpg'
        file_path = resource_filename('ProfileManager', resource_name)

    fp = basename(file_path)
    dp = dirname(file_path)

    return send_from_directory(dp, fp)
