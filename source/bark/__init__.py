# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .handler.distribute import Distribute

#: Top level handler responsible for relaying all logs to other handlers.
handle = Distribute()

