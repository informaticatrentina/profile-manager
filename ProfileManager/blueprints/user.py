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

from flask.ext.login import current_user, login_required

from flask.ext.principal import identity_changed, Identity


user = Blueprint('user', __name__,
                 template_folder='user/templates',
                 static_folder='user/static',
                 static_url_path='/user_static'  # TODO: be more modular
                 )

# TODO: how can we import the set from the current_app
from flask.ext.uploads import UploadSet, IMAGES

images = UploadSet("images", IMAGES)


# Property list that can be edited currently
prop_list = (
    'firstname', 'lastname', 'email', 'sex', 'location',
    'tags', 'website', 'biography',
)


def eve2wtf(data):
    """Convert the data from eve to a suitable format for wtf"""

    for i in prop_list:
        data.setdefault(i, None)

    if 'sex' in data and isinstance(data['sex'], list):
        data['sex'] = data['sex'][0]

    if 'tags' in data and isinstance(data['tags'], list):
        data['tags'] = ', '.join(data['tags'])

    x = type('new_dict', (object,), data)

    return x


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


def _patch_user(userid, data, headers={}):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s%s/' % (
        current_app.config['IM_URL'],
        '/users/',
        userid
        )
    rc = requestclient.patch(endpoint, data, auth=auth, headers=headers)
    return rc


def _post_tag(tag):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s' % (
        current_app.config['IM_URL'],
        '/tags/',
        )
    data = tag
    rc = requestclient.post(endpoint, data, auth=auth)
    return rc


def _post_schemes(scheme):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s' % (
        current_app.config['IM_URL'],
        '/schemes/',
        )
    data = scheme
    rc = requestclient.post(endpoint, data, auth=auth)
    return rc


def _generate_and_save_thumbnail(origin, destination, h, w):
    from PIL import Image,  ImageOps
    image = Image.open(origin)
    size = (w, h)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image.save(destination)

def _get_tags(tagname):
    auth = (current_app.config['IM_USER'], current_app.config['IM_PASSWORD'])
    endpoint = '%s%s' % (
        current_app.config['IM_URL'],
        '/tags/?where=name=="%s"' % tagname,
        )
    rc = requestclient.get(endpoint, auth=auth)
    return rc

@user.route('/')
def home():
    """
    The home page redirects to the fist page of user listing:
    :http:get:`/index/`
    """
    return redirect(url_for('auth.login'))


@user.route('/index/', defaults={'page': 1})
@user.route('/index/<int:page>')
def index(page):
    """
    Show a page listing the users paginated by 20 users

    :param page: the page number (optional, default 1)

    .. note::

        The sphinxcontrib.autohttp.flask do not group the routes
    """

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
        pages=pages,
        logged_user=current_user
        )


@user.route('/show/<userid>')
def show(userid):
    """
    Show a page with the user profile

    :param userid: the `user id`
    """

    userdata = _get_user(userid)

    if '_links' in userdata:
        del(userdata['_links'])

    return render_template(
        'user_show.html',
        user=userdata,
        logged_user=current_user)


@user.route('/show/<userid>/method')
def show_method(userid):
    """
    Show a page with the user profile with the method stuff

    :param userid: the `user id`
    """

    userdata = _get_user(userid)

    if '_links' in userdata:
        del(userdata['_links'])

    host = request.host

    return render_template(
        'user_method.html',
        user=userdata,
        logged_user=current_user,
        host=host)


@user.route('/show/<userid>/method_embed')
def show_method_embed(userid):
    """
    Show a page with the user profile with the embeded method stuff

    :param userid: the `user id`
    """

    userdata = _get_user(userid)

    if '_links' in userdata:
        del(userdata['_links'])

    return render_template(
        'user_method_embed.html',
        user=userdata,
        logged_user=current_user)


@user.route('/edit/<userid>', methods=['GET', 'POST'])
@login_required
def edit(userid):
    """Show a page for editing the user profile

    :param userid: the `user id`

    An user can edit only its own profile
    """

    if current_user.id != userid:
        return redirect(url_for('auth.login'))

    import os.path
    userdata = _get_user(userid)

    userobj = eve2wtf(userdata)

    form = UserProfileForm(request.form, obj=userobj)

    if request.method == 'POST' and form.validate():
        # Handle the photo upload
        if request.files.get('photo'):
            # TODO: respect original extension
            #
            # Note: it is not not a big problem, PIL handles different
            # format even if saved as .jpg
            name_original = "{}_original.{}".format(userid, 'jpg')

            # Remove old photo
            from os.path import exists
            from os import unlink

            if exists(images.path(name_original)):
                unlink(images.path(name_original))

                # Remove the old cached resized images
                base_name = "{}_".format(userid)
                base_path = images.path(base_name)
                from glob import glob
                files = glob('%s*[0-9].jpg' % (base_path))
                for file in files:
                    os.unlink(file)

            # Save the upload
            images.save(
                request.files.get('photo'),
                name=name_original)

        form.populate_obj(userobj)

        from json import dumps

        patch = {}
        for i in prop_list:
            patch[i] = userobj.__dict__[i]

        tags = [x.strip() for x in patch['tags'].split(',')]

        # Insert brutally the tags
        # TODO: handle the ,, zero lenght tag
        if tags[0]:
            for tag in tags:
                rc = _post_tag({'item1': dumps({'name': tag, 'slug': tag})})

        # As list!
        patch['sex'] = [patch['sex']]

        # Fix the tags
        if tags[0]:
            patch['tags'] = tags
        else:
            del patch['tags']

        # TODO: Temporary fix to get the save function properly into
        # both production and development version of the identity
        # manager
        if 'tags' in patch:
            del patch['tags']

        patchdict = {'key1': dumps(patch)}

        rc = _patch_user(
            userid,
            patchdict,
            headers={
                'If-Match': userobj.etag,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        )

        if rc.json()['key1']['status'] == 'OK':
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(userid))

            return redirect(url_for('.show', userid=userid))
        else:
            from flask import flash
            for message in rc.json()['key1']['issues']:
                flash(message)
            return redirect(url_for('.edit', userid=userid))

    if '_links' in userdata:
        del(userdata['_links'])

    return render_template(
        'user_edit.html',
        form=form,
        user=userobj,
        logged_user=current_user,
        title=_(u"Edit your profile"))


@user.route('/photo/<userid>/', defaults={'width': 80})
@user.route('/photo/<userid>/<int:width>')
def photo(userid, width):
    """
    Return a square user photo or the default one with the requested
    width

    :param userid: ``user id``
    :param width: optional width of the requested image (default 80)

    """

    from os.path import basename, dirname, exists

    from flask import send_from_directory

    name_original = "{}_original.{}".format(userid, 'jpg')
    name_resize = "{}_{}.{}".format(userid, width, 'jpg')

    file_path = images.path(name_resize)
    default_path = images.path(name_original)

    # Check for a cached image
    if not exists(file_path):
        if exists(default_path):
            # Generate cache
            _generate_and_save_thumbnail(
                images.path(default_path),
                images.path(file_path),
                width,
                width)
        else:
            # Return a copy the default image

            # Should we use redirect instead?  How browser cope with
            # redirect on images?  Yes we can also do that according
            # to:
            # http://stackoverflow.com/questions/3778347/is-it-ok-to-http-redirect-images
            from pkg_resources import resource_filename
            resource_name = 'blueprints/user/static/img/foto_anonima.jpg'
            default_path = resource_filename('ProfileManager', resource_name)
            _generate_and_save_thumbnail(
                images.path(default_path),
                images.path(file_path),
                width,
                width)


    fp = basename(file_path)
    dp = dirname(file_path)

    return send_from_directory(dp, fp, cache_timeout=10)
