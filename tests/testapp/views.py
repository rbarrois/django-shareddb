# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

import logging
import json

from django.db import transaction
from django import http

from . import models

logger = logging.getLogger(__name__)

def read(request):
    try:
        qs = (models.Something.objects
            .order_by('pk')
            .values('pk', 'data')
        )
        data = json.dumps(list(qs))
    except Exception as e:
        logger.error("Failed to get items from qs: %r", e)
        raise

    return http.HttpResponse(data, content_type='application/json')


@transaction.atomic
def atomic_read(request):
    return read(request)
