# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys

import bark
import bark.handler.stream
import bark.handler.email
import bark.handler.buffer
import bark.formatter.template
import bark.formatter.field
import bark.filterer.level
import bark.filterer.item


def configure(*args, **kw):
    '''Example of how to configure logging system.'''
    # Output to standard error stream.
    stderr_handler = bark.handler.stream.Stream(sys.stderr)
    stderr_formatter = bark.formatter.template.Template('{level}:{message}')
    stderr_handler.formatter = stderr_formatter

    stderr_filterer = bark.filterer.level.Level(min='warning', max=None)
    stderr_filterer |= bark.filterer.item.Item('user', True)
    stderr_handler.filterer = stderr_filterer

    bark.root.handlers['stderr'] = stderr_handler

    # Output to log file
    log_path = '/path/to/logfile.log'
    file_stream = open(log_path, 'a')
    file_handler = bark.handler.stream.Stream(file_stream)

    file_formatter = bark.formatter.field.Field([
        'date', 'level', 'name', 'message', '*'
    ])
    file_handler.formatter = file_formatter

    bark.root.handlers['file'] = file_handler

    # Send email on errors.
    email_handler = bark.handler.email.Email(
        'Error Report',
        'no-reply@bark.net',
        'support@bark.net'
    )

    def check_for_error(logs, buffer):
        '''Return True if any of the recent logs was an error message.'''
        for log in logs:
            if log.get('level') == 'error':
                return True

        return False

    email_buffer_handler = bark.handler.buffer.Buffer(
        email_handler,
        check_for_error,
        limit=30
    )

    bark.root.handlers['email'] = email_buffer_handler

