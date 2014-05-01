# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.db import utils
from django.db import backends


class DatabaseWrapper(backends.BaseDatabaseWrapper):
    def __init__(self, settings_dict, alias, **kwargs):
        if not settings_dict.get('INNER_ENGINE'):
            raise ImproperlyConfigured(
                "The shareddb.backends.shareddb database engine requires a 'INNER_ENGINE' setting.")

        # Thread sharing
        self.allow_thread_sharing = True
        kwargs['allow_thread_sharing'] = False

        # Load the inner module        
        inner_engine_module_name = settings_dict['INNER_ENGINE']
        inner_engine_module = utils.load_backend(inner_engine_module_name)
        self.inner_engine = inner_engine_module.DatabaseWrapper(settings_dict, alias, **kwargs)

    _NON_FORWARDED_ATTRS = [
        'allow_thread_sharing',
        'inner_engine',
    ]

    def __getattribute__(self, key):
        if key == '_NON_FORWARDED_ATTRS' or key in self._NON_FORWARDED_ATTRS:
            return super(DatabaseWrapper, self).__getattribute__(key)
        return getattr(self.inner_engine, key)
