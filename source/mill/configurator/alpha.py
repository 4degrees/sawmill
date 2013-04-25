# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys
import tempfile
from datetime import datetime

import mill
import mill.handler.stream
import mill.handler.email
import mill.handler.buffer
import mill.formatter.template
import mill.formatter.field
import mill.filterer.level
import mill.filterer.item


def configure(email_sender, email_recipients, level='info', filepath=None,
              *args, **kw):
    '''Alpha configurator.

    *level* will determine the minimum level to display on stderr. *filepath*
    can be used to set where the log file should be stored. It defaults to a
    temporary file named after the current date and time.

    '''
    # Output to standard error stream.
    stderr_handler = mill.handler.stream.Stream(sys.stderr)
    stderr_formatter = mill.formatter.template.Template('{level}:{message}\n')
    stderr_handler.formatter = stderr_formatter

    stderr_filterer = mill.filterer.level.Level(min=level, max=None)
    stderr_filterer |= mill.filterer.item.Item('user', True)
    stderr_handler.filterer = stderr_filterer

    mill.root.handlers['stderr'] = stderr_handler

    # Output to log file
    if filepath is None:
        prefix = datetime.now().strftime('mill-%Y_%m_%d-%H_%M_%S-')
        _, filepath = tempfile.mkstemp(prefix=prefix, suffix='.log')

    file_stream = open(filepath, 'a')
    file_handler = mill.handler.stream.Stream(file_stream)

    file_formatter = mill.formatter.field.Field([
        'timestamp', '*', 'name', 'level', 'message', 'traceback'
    ])
    file_handler.formatter = file_formatter

    mill.root.handlers['file'] = file_handler

    # Send email on errors.
    email_handler = mill.handler.email.Email(
        'smtp.example.com', 587,
        secure=(),
        formatter=mill.formatter.email.Email(
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

    email_buffer_handler = mill.handler.buffer.Buffer(
        email_handler,
        check_for_error,
        limit=30
    )

    mill.root.handlers['email'] = email_buffer_handler

