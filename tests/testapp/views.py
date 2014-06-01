# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

import logging
import json

from django.db import transaction
from django import http

from . import models

logger = logging.getLogger(__name__)


def log_exceptions(view):
    """Simple decorator to get meaningful error logs in tests."""
    def decorated(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except Exception as e:
            logger.exception("Error in %s.%s: %r", view.__module__, view.__name__, e)
            raise
    return decorated


@log_exceptions
def read(request):
    qs = (models.Something.objects
        .order_by('pk')
        .values('pk', 'data')
    )
    data = json.dumps(list(qs))
    return http.HttpResponse(data, content_type='application/json')


@log_exceptions
@transaction.atomic
def atomic_read(request):
    return read(request)
