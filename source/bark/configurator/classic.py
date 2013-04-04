# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import tempfile
from datetime import datetime


def configure(level='info', filepath=None, *args, **kw):
    '''Configure the logging system in a classic manner.

    *level* will determine the minimum level to display on stderr. *filepath*
    can be used to set where the log file should be stored. It defaults to a
    temporary file named after the current date and time.

    '''
    import sys
    import bark
    from bark.handler.stream import Stream
    from bark.filterer.level import Level
    from bark.formatter.field import Field

    stderr_handler = Stream(
        sys.stderr,
        filterer=Level(min=level, max=None),
        formatter=Field(keys=['level', 'name', 'message'], template='{value}')
    )
    bark.handler.handlers['stderr'] = stderr_handler

    if filepath is None:
        prefix = datetime.now().strftime('bark-%Y_%m_%d-%H_%M_%S-')
        _, filepath = tempfile.mkstemp(prefix=prefix, suffix='.log')

    file_descriptor = open(filepath, 'a')
    file_handler = Stream(
        file_descriptor,
        filterer=Level(min=None, max=None),
        formatter=Field(keys=['level', 'name', 'message'])
    )
    bark.handler.handlers['file'] = file_handler

