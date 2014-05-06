# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

from django.db import models

class Something(models.Model):
    data = models.CharField(max_length=10)
