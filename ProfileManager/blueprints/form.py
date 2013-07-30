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
Helper Forms
============

TODO: replace this line with proper project description.
'''

from flask.ext.wtf import (
    file_allowed,
    FileField,
    Form,
    PasswordField,
    TextAreaField,
    TextField,
    validators,
    )


from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.babelex import lazy_gettext as _


images = UploadSet("images", IMAGES)


class TextFieldHelp(TextField):

    def __init__(self, *args, **kwargs):
        self.extra_description = kwargs.pop('extra_description', "")
        return super(TextFieldHelp, self).__init__(*args, **kwargs)


class TextAreaFieldHelp(TextAreaField):

    def __init__(self, *args, **kwargs):
        self.extra_description = kwargs.pop('extra_description', "")
        return super(TextAreaFieldHelp, self).__init__(*args, **kwargs)


class FileFieldHelp(FileField):

    def __init__(self, *args, **kwargs):
        self.extra_description = kwargs.pop('extra_description', "")
        return super(FileFieldHelp, self).__init__(*args, **kwargs)


class UserProfileForm(Form):
    first_name = TextField(
        _(u"First Name"),
        [validators.Length(min=1, max=132)],
        description=_(u"First Name"))
    last_name = TextField(
        _(u"Last Name"),
        [validators.Length(min=1, max=132)],
        description=_(u"Last Name"))
    email = TextField(
        _(u"Email Address"),
        [validators.Length(min=4, max=132)],
        description=_(u"Your email Address"))
    location = TextFieldHelp(
        _(u"Location"),
        [validators.Length(min=1, max=132)],
        description=_(u"Location"),
        extra_description=_(u"Where are you?"))
    tags = TextFieldHelp(
        _(u"Tags"),
        description=_(u"Tags"),
        extra_description=_(u"What are your personal interests?"))
    website = TextFieldHelp(
        _(u"Website"),
        description=_(u"Website"),
        extra_description=_(u"Do you have an homepage or a blog?"))
    bio = TextAreaFieldHelp(
        _(u"Biography"),
        [validators.Length(min=0, max=150)],
        extra_description=_(u"Tell about you in 150 chars"))
    avatar = FileFieldHelp(
        _(u"Your Photo"),
        [file_allowed(images, _(u"Images only!"))],
        description=_(u"Your Photo"),
        extra_description=_(u"Maximum size allowed 1MB."
                            " Allowed formats: jpg and png"))
    old_password = PasswordField(_(u"Old Password"),
                                 description=_(u"Old Password"))
    new_password = PasswordField(
        _(u"New Password"),
        [
            validators.Required(),
            validators.EqualTo(
                'confirm',
                message=_(u"Passwords must match"))
        ],
        description=_(u"Password"))
    con_password = PasswordField(
        _(u"Repeat Password"),
        description=_(u"Repeat Password"))
