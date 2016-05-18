# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys

import sawmill
import sawmill.handler.stream
import sawmill.handler.email
import sawmill.handler.buffer
import sawmill.formatter.template
import sawmill.formatter.field
import sawmill.filterer.level
import sawmill.filterer.item


def configure(*args, **kw):
    '''Example of how to configure logging system.'''
    # Output to standard error stream.
    stderr_handler = sawmill.handler.stream.Stream(sys.stderr)
    stderr_formatter = sawmill.formatter.template.Template('{level}:{message}')
    stderr_handler.formatter = stderr_formatter

    stderr_filterer = sawmill.filterer.level.Level(min='warning', max=None)
    stderr_filterer |= sawmill.filterer.item.Item('user', True)
    stderr_handler.filterer = stderr_filterer

    sawmill.root.handlers['stderr'] = stderr_handler

    # Output to log file
    log_path = '/path/to/logfile.log'
    file_stream = open(log_path, 'a')
    file_handler = sawmill.handler.stream.Stream(file_stream)

    file_formatter = sawmill.formatter.field.Field([
        'timestamp', 'level', 'name', 'message', '*'
    ])
    file_handler.formatter = file_formatter

    sawmill.root.handlers['file'] = file_handler

    # Send email on errors.
    email_handler = sawmill.handler.email.Email(
        'Error Report',
        'no-reply@sawmill.net',
        'support@sawmill.net'
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

