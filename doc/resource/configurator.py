# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys

import mill
import mill.handler.stream
import mill.handler.email
import mill.handler.buffer
import mill.formatter.template
import mill.formatter.field
import mill.filterer.level
import mill.filterer.item


def configure(*args, **kw):
    '''Example of how to configure logging system.'''
    # Output to standard error stream.
    stderr_handler = mill.handler.stream.Stream(sys.stderr)
    stderr_formatter = mill.formatter.template.Template('{level}:{message}')
    stderr_handler.formatter = stderr_formatter

    stderr_filterer = mill.filterer.level.Level(min='warning', max=None)
    stderr_filterer |= mill.filterer.item.Item('user', True)
    stderr_handler.filterer = stderr_filterer

    mill.root.handlers['stderr'] = stderr_handler

    # Output to log file
    log_path = '/path/to/logfile.log'
    file_stream = open(log_path, 'a')
    file_handler = mill.handler.stream.Stream(file_stream)

    file_formatter = mill.formatter.field.Field([
        'timestamp', 'level', 'name', 'message', '*'
    ])
    file_handler.formatter = file_formatter

    mill.root.handlers['file'] = file_handler

    # Send email on errors.
    email_handler = mill.handler.email.Email(
        'Error Report',
        'no-reply@mill.net',
        'support@mill.net'
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

