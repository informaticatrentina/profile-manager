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
Test for ProfileManager user blueprint
======================================

'''

try:
    import unittest2 as unittest
except ImportError:
    # NOQA
    import unittest


from ProfileManager import app as ProfileManagerApp


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ProfileManagerApp.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_user_home(self):
        '''Check the home template'''
        request = self.app.get('/', method='GET')
        self.assertEqual(request.status_code, 302)

    def test_user_index(self):
        '''Check the index template'''
        request = self.app.get('/index/', method='GET')
        self.assertEqual(request.status_code, 200)
        self.assertIn(u'Test User List', request.get_data(as_text=True))

    def test_user_show(self):
        '''Check the user show template'''
        request = self.app.get('/show/uid', method='GET')
        self.assertEqual(request.status_code, 200)
        self.assertIn(u'foto_anonima', request.get_data(as_text=True))

    def test_user_edit(self):
        '''Check the user edit template'''
        request = self.app.get('/edit/uid', method='GET')
        self.assertEqual(request.status_code, 200)
        self.assertIn(u'Racconta', request.get_data(as_text=True))

    def test_user_edit_post(self):
        '''Check the user edit template'''
        request = self.app.post('/edit/uid', method='POST')
        self.assertEqual(request.status_code, 200)
        self.assertIn(u'Racconta', request.get_data(as_text=True))
