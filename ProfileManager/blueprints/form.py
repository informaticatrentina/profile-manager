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
    Form,
)

from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    TextAreaField,
    TextField,
    validators,
)

from flask.ext.wtf.file import FileAllowed, FileField


from flask.ext.babelex import lazy_gettext as _

# TODO: how can we import the set from the current_app
from flask.ext.uploads import UploadSet, IMAGES


images = UploadSet("images", IMAGES)


class TextFieldHelp(TextField):

    def __init__(self, *args, **kwargs):
        self.extra_description = kwargs.pop('extra_description', "")
        return super(TextFieldHelp, self).__init__(*args, **kwargs)


class TextAreaFieldHelp(TextAreaField):

    def __init__(self, *args, **kwargs):
        self.extra_description = kwargs.pop('extra_description', "")
        self.extra_maxlength = kwargs.pop('extra_maxlength', 100)
        return super(TextAreaFieldHelp, self).__init__(*args, **kwargs)


class FileFieldHelp(FileField):

    def __init__(self, *args, **kwargs):
        self.extra_description = kwargs.pop('extra_description', "")
        return super(FileFieldHelp, self).__init__(*args, **kwargs)


class UserProfileForm(Form):
    firstname = TextField(
        _(u"First Name"),
        [validators.Length(min=1, max=132)],
        description=_(u"First Name"))

    lastname = TextField(
        _(u"Last Name"),
        [validators.Length(min=1, max=132)],
        description=_(u"Last Name"))

    email = TextField(
        _(u"Email Address"),
        [validators.Email()],
        description=_(u"Your email Address"))

    sex = SelectField(
        _(u'Sex'),
        [validators.AnyOf(("M", "F"), message=_(u"Please select your Sex"))],
        choices=[
            ("U", _(u"Select Sex")),
            ("M", _(u"Male")),
            ("F", _(u"Female")),
        ],
        description=_(u"Select Sex"))

    location = TextFieldHelp(
        _(u"Location"),
        [validators.Length(min=0, max=132)],
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

    biography = TextAreaFieldHelp(
        _(u"Biography"),
        [validators.Length(min=0, max=150)],
        extra_description=_(u"Tell about you in 150 chars"),
        extra_maxlength=150)

    photo = FileFieldHelp(
        _(u"Your Photo"),
        [FileAllowed(images, _(u"Images only!"))],
        description=_(u"Your Photo"),
        extra_description=_(u"Maximum size allowed 1MB."
                            " Allowed formats: jpg and png"))

    old_password = PasswordField(
        _(u"Old Password"),
        description=_(u"Old Password"))

    new_password = PasswordField(
        _(u"New Password"),
        [
            validators.EqualTo(
                'old_password',
                message=_(u"Passwords must match"))
        ],
        description=_(u"Password"))

    con_password = PasswordField(
        _(u"Repeat Password"),
        description=_(u"Repeat Password"))
