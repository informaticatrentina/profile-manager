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
        # TODO: put the data back to the im
        return redirect(url_for('/'))  # TODO view

    if '_links' in user:
        del(user['_links'])

    return render_template(
        'user_edit.html',
        form=form,
        user=user,
        title=_(u"Edit your profile"))
