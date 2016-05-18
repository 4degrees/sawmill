# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys
import tempfile
from datetime import datetime

import sawmill
import sawmill.handler.stream
import sawmill.handler.email
import sawmill.handler.buffer
import sawmill.formatter.template
import sawmill.formatter.field
import sawmill.filterer.level
import sawmill.filterer.item


def configure(email_sender, email_recipients, level='info', filepath=None,
              *args, **kw):
    '''Alpha configurator.

    *level* will determine the minimum level to display on stderr. *filepath*
    can be used to set where the log file should be stored. It defaults to a
    temporary file named after the current date and time.

    '''
    # Output to standard error stream.
    stderr_handler = sawmill.handler.stream.Stream(sys.stderr)
    stderr_formatter = sawmill.formatter.template.Template(
        '{level}:{message}\n'
    )
    stderr_handler.formatter = stderr_formatter

    stderr_filterer = sawmill.filterer.level.Level(min=level, max=None)
    stderr_filterer |= sawmill.filterer.item.Item('user', True)
    stderr_handler.filterer = stderr_filterer

    sawmill.root.handlers['stderr'] = stderr_handler

    # Output to log file
    if filepath is None:
        prefix = datetime.now().strftime('sawmill-%Y_%m_%d-%H_%M_%S-')
        _, filepath = tempfile.mkstemp(prefix=prefix, suffix='.log')

    file_stream = open(filepath, 'a')
    file_handler = sawmill.handler.stream.Stream(file_stream)

    file_formatter = sawmill.formatter.field.Field([
        'timestamp', '*', 'name', 'level', 'message', 'traceback'
    ])
    file_handler.formatter = file_formatter

    sawmill.root.handlers['file'] = file_handler

    # Send email on errors.
    email_handler = sawmill.handler.email.Email(
        'smtp.example.com', 587,
        secure=(),
        formatter=sawmill.formatter.email.Email(
            'Error Report',
            email_sender,
            email_recipients
        )
    )

    def check_for_error(logs, buffer):
        '''Return True if any of the recent logs was an error message.'''
        for log in logs:
            if log.get('level') == 'error':
                return True

        return False

    email_buffer_handler = sawmill.handler.buffer.Buffer(
        email_handler,
        check_for_error,
        limit=30
    )

    sawmill.root.handlers['email'] = email_buffer_handler

