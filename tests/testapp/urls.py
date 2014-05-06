# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^read/$', views.read),
    url(r'^atomic-read/$', views.atomic_read),
)
