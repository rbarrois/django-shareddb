# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('tests.testapp.urls')),
)
