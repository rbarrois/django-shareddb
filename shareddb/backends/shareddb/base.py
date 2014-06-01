# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.


from django.core.exceptions import ImproperlyConfigured
from django.db import utils
from django.db import backends


from ... import threlegate


# Only spawn one thread per DB alias, and keep them in this global variable.
DELEGATES = {}


def make_delegate(settings_dict, alias):
    key = alias
    if key not in DELEGATES:
        delegate = threlegate.DelegateQueue(name='delegate-%s' % alias)
        DELEGATES[key] = delegate
        # Start once registered, in case something is also trying to spawn the alias.
        delegate.start()

    return DELEGATES[key]


# Store a single wrapper per DatabaseWrapper, too.
SHARED_WRAPPERS = {}


class DelegatingDatabaseWrapper(backends.BaseDatabaseWrapper):
    """Abstract DatabaseWrapper, delegates functions to its DelegateQueue."""
    def __init__(self, delegate, settings_dict, alias, **kwargs):
        self.delegate = delegate
        super(DelegatingDatabaseWrapper, self).__init__(settings_dict, alias, **kwargs)
        self.allow_thread_sharing = False

    # DB object creation
    # ==================

    def create_cursor(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).create_cursor)

    def get_new_connection(self, conn_params):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).get_new_connection, conn_params)

    # Commit-related, with validate_thread_sharing()
    # ==============================================

    def cursor(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).cursor)

    def commit(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).commit)

    def rollback(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).rollback)

    def close(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).close)

    # Savepoint-related
    # =================

    def savepoint(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).savepoint)

    def savepoint_rollback(self, sid):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).savepoint_rollback, sid)

    def savepoint_commit(self, sid):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).savepoint_commit, sid)

    def clean_savepoints(self):
        return self.delegate.execute(super(DelegatingDatabaseWrapper, self).clean_savepoints)


def make_wrapper(settings_dict, alias, **kwargs):
    """Create a wrapper for a shareddb.backends.shareddb engine.

    Generates a delegating wrapper at call-time.
    """

    if not settings_dict.get('INNER_ENGINE'):
        raise ImproperlyConfigured(
            "The shareddb.backends.shareddb database engine requires a 'INNER_ENGINE' setting.")

    delegate = make_delegate(settings_dict, alias)

    # Load the inner module        
    inner_engine_module_name = settings_dict['INNER_ENGINE']
    inner_engine_module = utils.load_backend(inner_engine_module_name)

    class InnerDatabaseWrapper(DelegatingDatabaseWrapper, inner_engine_module.DatabaseWrapper):
        pass

    return delegate.execute(InnerDatabaseWrapper, delegate, settings_dict, alias, **kwargs)


def DatabaseWrapper(settings_dict, alias, **kwargs):
    """Generate a DelegatingDatabaseWrapper for the given alias.

    Django expects this class to exist and to be callable.
    """
    if alias not in SHARED_WRAPPERS:
        SHARED_WRAPPERS[alias] = make_wrapper(settings_dict, alias, **kwargs)
    return SHARED_WRAPPERS[alias]
