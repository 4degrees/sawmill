# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .handler.distribute import Distribute

#: Top level handler responsible for relaying all logs to other handlers.
handler = Distribute()
handlers = handler.handlers
handle = handler.handle

#: Log levels ordered by severity. Do not rely on the index of the level name
# as it may change depending on the configuration.
levels = [
    'debug',
    'info',
    'warning',
    'error'
]

