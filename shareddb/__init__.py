# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

__version__ = '0.1.2'
__author__ = "Raphaël Barrois <raphael.barrois+django-shareddb@polytechnique.org>"

SHAREDDB_ENGINE = 'shareddb.backends.shareddb'


def patch_databases(orig_setting, whitelist=(), blacklist=()):
    new_settings = {}
    for alias, old_alias_settings in orig_setting.items():
        alias_settings = dict(old_alias_settings)
        if alias not in blacklist and (not whitelist or alias in whitelist):
            alias_settings['INNER_ENGINE'] = alias_settings['ENGINE']
            alias_settings['ENGINE'] = SHAREDDB_ENGINE
        new_settings[alias] = alias_settings

    return new_settings
