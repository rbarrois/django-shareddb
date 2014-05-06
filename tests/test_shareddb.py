# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.


import requests

from shareddb import testcase

from .testapp import models

class BaseTest(testcase.LiveServerTestCase):
    def test_simple_db_access(self):
        self.assertEqual(0, models.Something.objects.count())

    def test_read_none(self):
        response = requests.get(self.live_server_url + '/read/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'[]', response.content)

    def test_read_exists(self):
        s = models.Something.objects.create(data='ex1')
        response = requests.get(self.live_server_url + '/read/')
        self.assertEqual(200, response.status_code)

        data = response.json()
        self.assertEqual([{'pk': s.pk, 'data': 'ex1'}], data)

    def test_atomic_read_none(self):
        response = requests.get(self.live_server_url + '/atomic-read/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'[]', response.content)

    def test_atomic_read_exists(self):
        s = models.Something.objects.create(data='ex1')
        response = requests.get(self.live_server_url + '/atomic-read/')
        self.assertEqual(200, response.status_code)

        data = response.json()
        self.assertEqual([{'pk': s.pk, 'data': 'ex1'}], data)
