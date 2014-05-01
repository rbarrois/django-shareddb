# -*- coding: utf-8 -*-

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
