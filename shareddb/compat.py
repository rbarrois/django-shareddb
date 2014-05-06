# -*- coding: utf-8 -*-
# Copyright (c) 2014 Raphaël Barrois
# This software is distributed under the two-clause BSD license.

import sys

if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue
